# indeed_bot.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # Initialize Chrome browser using webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # Open Indeed's homepage
    driver.get("https://www.indeed.com")
    
    # Let the browser stay open for 10 seconds so you can see it
    import time
    time.sleep(10)
    
    # Close the browser after 10 seconds
    driver.quit()

if __name__ == "__main__":
    main()
