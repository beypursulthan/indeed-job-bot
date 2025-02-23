# indeed-job-bot
Automatically apply for jobs in indeed

```markdown:README.md
# Indeed Job Bot

An automated tool that helps you apply for jobs on Indeed using the "Easy Apply" feature. The bot supports both English and German Indeed websites.

## Features

- Automated job searching based on customizable filters
- Supports Easy Apply/Schnellbewerbung applications
- Handles both English and German Indeed interfaces
- Automatic popup handling
- Smart retry mechanism with exponential backoff
- Visual feedback for button clicks and interactions

## Prerequisites

1. Python 3.7 or higher
2. Chrome browser installed
3. Basic understanding of command line operations

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/indeed-job-bot.git
cd indeed-job-bot
```

2. Install required packages:
```bash
pip install undetected-chromedriver selenium
```

## Configuration

1. Create or modify `job_filters.txt` with your job search criteria:
```
job_title=Your Job Title
location=Your Location
job_type=full-time, part-time, contract, internship
```

Note: For job_type, you can use any combination of: full-time, part-time, contract, internship

## Usage

1. Set up your Indeed profile:
   - Create an Indeed account if you don't have one
   - Upload your resume
   - Complete your profile
   - Prepare any standard answers for common application questions

2. Configure your search filters:
   - Edit `job_filters.txt` with your desired job criteria
   - Make sure the location and job title are accurate

3. Run the bot:
```bash
python indeed_bot.py
```

4. When the Chrome browser opens:
   - Log into your Indeed account manually. I recommend using the "login with the code" option instead of the      normal login with password.
   - Press Enter in the terminal to start the automation
   - The bot will begin searching and applying for jobs

5. Monitor the process:
   - The bot will provide real-time feedback in the terminal
   - It will show which jobs it's applying to and any errors encountered
   - The process continues until all available jobs are processed

## Important Notes

- The bot only applies to jobs with the "Easy Apply" option
- It's recommended to monitor the bot while it's running
- Some jobs may require additional information that the bot cannot provide
- The bot includes waiting periods to avoid being flagged as automated
- If you encounter any errors, check the terminal output for details

## Troubleshooting

- If the bot fails to start, ensure Chrome is updated to the latest version
- If login issues occur, try logging in manually and restart the bot
- If the bot isn't finding jobs, verify your job_filters.txt configuration
- For any other issues, check the error messages in the terminal

## Legal Disclaimer

This bot is for educational purposes only. Using automated tools to apply for jobs may be against Indeed's terms of service. Use at your own risk and responsibility.

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```

If you are beginner, use the cursor ai platform to run the code and use the terminal. Cursor has a built in AI chat option. You can ask it doubts and troubleshoots in natural language.
