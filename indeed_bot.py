import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

def read_job_filters(file_path="job_filters.txt"):
    """Reads job filters from a text file."""
    filters = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                if "=" in line and not line.strip().startswith("#"):
                    key, value = line.strip().split("=", 1)
                    filters[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please create the file with job filters.")
        exit()
    return filters

def search_jobs(driver, filters):
    """Search for jobs using the provided filters."""
    try:
        wait = WebDriverWait(driver, 10)
        
        # Fill in job title
        what_field = wait.until(EC.presence_of_element_located((By.ID, "text-input-what")))
        what_field.clear()
        what_field.send_keys(filters['job_title'])
        
        # Fill in location
        where_field = driver.find_element(By.ID, "text-input-where")
        where_field.clear()
        where_field.send_keys(filters['location'])
        
        # Submit search
        what_field.send_keys(Keys.RETURN)
        time.sleep(3)  # Wait for results to load
        
        # German job type translations
        job_type_translations = {
            'full-time': 'vollzeit',
            'part-time': 'teilzeit',
            'contract': 'befristet',
            'internship': 'praktikum'
        }
        
        # Filter by job types if specified
        if 'job_type' in filters:
            job_types = [jtype.strip() for jtype in filters['job_type'].split(',')]
            for job_type in job_types:
                try:
                    # Use German translation if available
                    german_type = job_type_translations.get(job_type.lower(), job_type)
                    job_type_button = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, f"//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{german_type}')]")
                    ))
                    highlight_element(driver, job_type_button)
                    job_type_button.click()
                    print(f"Applied filter: {german_type}")
                    time.sleep(1)
                except TimeoutException:
                    print(f"Could not find job type filter for: {job_type} ({german_type})")
                except Exception as e:
                    print(f"Error applying job type filter {job_type}: {e}")

    except Exception as e:
        print(f"Error during job search: {e}")

def is_easy_apply(driver):
    """Check if the job has Indeed's Easy Apply button (both English and German)."""
    try:
        # Try multiple ways to find the button (just as helpers to locate potential buttons)
        buttons = []
        selectors = [
            (By.ID, "indeedApplyButton"),
            (By.CSS_SELECTOR, "button[class*='css-km0m34']"),
            (By.CSS_SELECTOR, "button[aria-label*='Schnellbewerbung']"),
            (By.CSS_SELECTOR, "button[aria-label*='Quick Apply']"),
            (By.CSS_SELECTOR, "button")  # Fallback to check all buttons
        ]
        
        print("\nChecking for Easy Apply button...")
        # Collect all potential buttons
        for by, selector in selectors:
            try:
                elements = driver.find_elements(by, selector)
                buttons.extend(elements)
            except:
                continue
                
        print(f"Found {len(buttons)} buttons to check")
        
        # Check each button for either criteria: color OR text
        for button in buttons:
            if not button.is_displayed():
                continue
                
            try:
                # Check the color
                bg_color = button.value_of_css_property("background-color")
                print(f"Button background color: {bg_color}")
                
                # Check the text
                button_text = button.text.lower()
                if not button_text:
                    try:
                        wrapper = button.find_element(By.CLASS_NAME, "jobsearch-IndeedApplyButton-contentWrapper")
                        button_text = wrapper.text.lower()
                    except:
                        try:
                            span = button.find_element(By.CSS_SELECTOR, "span.jobsearch-IndeedApplyButton-newDesign")
                            button_text = span.text.lower()
                        except:
                            continue
                
                print(f"Button text: {button_text}")
                
                # If EITHER color OR text matches, we found our button!
                if ("rgb(37, 87, 167)" in bg_color or "#2557a7" in bg_color or 
                    "schnellbewerbung" in button_text):
                    print("Found matching button!")
                    return True
            except Exception as e:
                print(f"Error checking button: {e}")
                continue
        
        print("No matching button found")
        return False
    except Exception as e:
        print(f"Error checking for easy apply: {e}")
        return False

def highlight_element(driver, element):
    """Highlight an element before clicking it."""
    try:
        # Move mouse to element with visual feedback
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.perform()
        
        # Add a brief pause to make the movement visible
        time.sleep(0.5)
        
        # Optional: Change element background color for visibility
        driver.execute_script("arguments[0].style.backgroundColor = 'yellow'", element)
        time.sleep(0.5)
        driver.execute_script("arguments[0].style.backgroundColor = ''", element)
    except:
        pass  # If highlighting fails, continue without it

def apply_to_job(driver):
    """Apply to a job using Indeed Easy Apply/Schnellbewerbung."""
    try:
        # Try to find the button using the same successful selectors from is_easy_apply
        apply_button = None
        
        # First try the ID
        try:
            apply_button = driver.find_element(By.ID, "indeedApplyButton")
            if apply_button.is_displayed() and "schnellbewerbung" in apply_button.text.lower():
                print("Found button by ID")
        except:
            pass
            
        # If not found, try by class and color
        if not apply_button:
            try:
                buttons = driver.find_elements(By.CSS_SELECTOR, "button[class*='css-km0m34']")
                for button in buttons:
                    if button.is_displayed():
                        bg_color = button.value_of_css_property("background-color")
                        button_text = button.text.lower()
                        
                        # Check for either blue color or Schnellbewerbung text
                        if ("rgb(37, 87, 167)" in bg_color or "#2557a7" in bg_color or 
                            "schnellbewerbung" in button_text):
                            apply_button = button
                            print(f"Found button with color: {bg_color} and text: {button_text}")
                            break
            except Exception as e:
                print(f"Error finding button by class/color: {e}")
                
        if not apply_button:
            print("Could not find apply button")
            return False
            
        print("Clicking apply button...")
        highlight_element(driver, apply_button)
        apply_button.click()
        time.sleep(2)

        # Switch to the new tab if opened
        original_window = driver.current_window_handle
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        # Wait for form to load
        time.sleep(3)

        # List of button text to look for (both German and English)
        continue_buttons_text = [
            'weiter',  # Further
            'fortfahren',  # Continue
            'fortsetzung',  # Continue
            'fortsetzen',  # Continue
            'next',
            'continue',
            'submit',
            'apply',
            'senden',  # Send
            'bewerben',  # Apply
            'bewerbung absenden',  # Send application
            'jetzt bewerben',  # Apply now
            'trotzdem bewerben'  # Apply anyway
        ]

        # Keep clicking continue buttons until we see success message or run out of buttons
        max_steps = 10  # Maximum number of form steps
        for step in range(max_steps):
            try:
                # Look for success message
                success_texts = [
                    'bewerbung gesendet',  # Application sent
                    'application submitted',
                    'successfully submitted',
                    'thank you for applying'
                ]
                
                page_text = driver.page_source.lower()
                if any(text in page_text for text in success_texts):
                    print("Application successfully submitted!")
                    driver.close()  # Close the application tab
                    driver.switch_to.window(original_window)  # Switch back to main window
                    return True

                # Try to find and click the next button
                button_found = False
                
                # Special check for "Weiter" button with display: flex
                try:
                    weiter_buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='button']")
                    for button in weiter_buttons:
                        if button.is_displayed() and button.is_enabled():
                            display_style = driver.execute_script(
                                "return window.getComputedStyle(arguments[0]).display", 
                                button
                            )
                            if display_style == 'flex' and button.text.lower() == 'weiter':
                                highlight_element(driver, button)
                                button.click()
                                print("Clicked 'Weiter' button")
                                button_found = True
                                time.sleep(2)
                                break
                except Exception as e:
                    print(f"Error checking for Weiter button: {e}")

                # If "Weiter" button not found, try other buttons
                if not button_found:
                    for button_text in continue_buttons_text:
                        try:
                            buttons = driver.find_elements(By.XPATH, 
                                f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{button_text}')]")
                            
                            for button in buttons:
                                if button.is_displayed() and button.is_enabled():
                                    highlight_element(driver, button)
                                    button.click()
                                    print(f"Clicked button: {button_text}")
                                    button_found = True
                                    time.sleep(2)
                                    break
                            if button_found:
                                break
                        except:
                            continue

                if not button_found:
                    print("No more buttons found")
                    driver.close()
                    driver.switch_to.window(original_window)
                    return False

            except Exception as e:
                print(f"Error in application step {step}: {e}")
                driver.close()
                driver.switch_to.window(original_window)
                return False

        print("Reached maximum number of steps without completing application")
        driver.close()
        driver.switch_to.window(original_window)
        return False

    except Exception as e:
        print(f"Error during application: {e}")
        try:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            pass
        return False

def close_popups(driver):
    """Close any pop-ups that might appear."""
    try:
        # List of common pop-up selectors (add more as needed)
        popup_selectors = [
            "[class*='popup-close']",
            "[class*='close-button']",
            "[class*='modal-close']",
            "[aria-label='Close']",
            "[class*='newsletter'] button[class*='close']",
            ".icl-CloseButton",
            "#popover-x",
            "#popover-foreground .popover-x-button-close"
        ]

        for selector in popup_selectors:
            try:
                close_buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                for button in close_buttons:
                    if button.is_displayed():
                        highlight_element(driver, button)
                        button.click()
                        time.sleep(0.5)
            except:
                continue

    except Exception as e:
        print(f"Error handling popups: {e}")

def click_job_card(driver, job_card):
    """Safely click a job card with proper waiting and scrolling."""
    try:
        # Scroll the job card into view
        driver.execute_script("arguments[0].scrollIntoView(true);", job_card)
        time.sleep(1)  # Wait for scroll to complete
        
        # Wait for the card to be clickable
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable(job_card))
        
        # Highlight and click
        highlight_element(driver, job_card)
        job_card.click()
        time.sleep(2)  # Wait for job details to load
        return True
    except Exception as e:
        print(f"Error clicking job card: {e}")
        return False

def retry_with_backoff(func, max_retries=3):
    """Retry a function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "invalid session" in str(e).lower():
                if attempt == max_retries - 1:  # Last attempt
                    raise  # Re-raise the last exception
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise  # Re-raise other exceptions immediately

def main():
    """Launch an undetected Chrome session and automate job applications."""
    try:
        # Read job filters
        filters = read_job_filters()
        
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        driver = uc.Chrome(options=options, version_main=133)
        wait = WebDriverWait(driver, 10)
        
        # Open Indeed
        driver.get("https://www.indeed.com/")
        time.sleep(2)
        
        input("Press Enter after logging in to continue...")
        print("Login detected. Proceeding with job search...")
        
        # Search for jobs
        search_jobs(driver, filters)
        
        # Process job listings
        jobs_applied = 0
        while True:
            try:
                # Wait for job cards to load and get fresh references
                time.sleep(2)
                job_cards = wait.until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "job_seen_beacon"))
                )
                
                for i in range(len(job_cards)):
                    try:
                        # Get fresh reference to job cards
                        job_cards = wait.until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "job_seen_beacon"))
                        )
                        job_card = job_cards[i]
                        
                        # Close any popups
                        close_popups(driver)
                        
                        # Try to click the job card safely
                        if not click_job_card(driver, job_card):
                            continue
                        
                        # Close popups that might appear after clicking
                        close_popups(driver)
                        
                        # Check if it's an Easy Apply job
                        if retry_with_backoff(lambda: is_easy_apply(driver)):
                            print("Found Easy Apply job, attempting to apply...")
                            if retry_with_backoff(lambda: apply_to_job(driver)):
                                jobs_applied += 1
                                print(f"Successfully applied! Total applications: {jobs_applied}")
                        else:
                            print("Skipping non-Easy Apply job")
                        
                        time.sleep(1)
                    except IndexError:
                        print("Reached end of current job cards")
                        break
                    except Exception as e:
                        print(f"Error processing job card: {e}")
                        continue
                
                # Try to click "Next" button
                try:
                    next_button = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Next']"))
                    )
                    if not next_button.is_enabled():
                        print("Reached last page")
                        break
                    next_button.click()
                    time.sleep(3)
                except NoSuchElementException:
                    print("No more pages")
                    break
                except Exception as e:
                    print(f"Error navigating to next page: {e}")
                    break
                    
            except Exception as e:
                print(f"Error processing page: {e}")
                break
        
        print(f"\nApplication process completed. Applied to {jobs_applied} jobs.")
        input("Press Enter to close the browser...")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    main()
