# Weather Check Agent

Weather Check Agent is a lightweight automation tool built with Python and Selenium that automates a daily task—retrieving the current weather for a specified city. Instead of manually checking the weather online, this agent opens Google’s weather search page, extracts the current weather condition, and compares it with an expected condition provided by the user. 

**NOTE: PLEASE CHECK THE MASTER BRANCH FOR THE ENTIRE CODE**

## Problem Statement

Many users perform daily weather checks manually to plan their day. Weather Check Agent automates this routine by:
- Accepting a city name (e.g., "New York") and an expected weather condition (e.g., "Sunny") as input.
- Navigating to Google’s weather search results for that city.
- Extracting the current weather condition from the page.
- Comparing the actual weather condition with the expected condition and outputting whether they match.

This simple automation reduces manual effort and provides a quick way to verify weather conditions each day.

## Features

- **Automated Weather Retrieval:** Opens a browser and fetches the current weather for a given city.
- **Validation:** Compares the extracted weather condition with the expected condition.
- **Command-Line Interface:** Run the script with a single command.
- **Simple & Extendable:** A basic framework that can be adapted for other browser automation tasks.

## Requirements

- **Python 3.x**
- **Selenium:** Install using pip:
  ```bash
  pip install selenium

**WebDriver:**
For Chrome, download ChromeDriver.
For Firefox, download GeckoDriver.
Note: With Selenium 4.6+, Selenium Manager can automatically manage drivers.

## Installation
1. Clone the Repository:
```bash
git clone -b master https://github.com/ruchirk22/weather-check-agent.git
cd weather-check-agent
```
2. (Optional) Create and Activate a Virtual Environment (Windows):
```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```
3. Install Dependencies:
 ```bash
 pip install selenium webdriver-manager
 ```
## Usage
Run the project from the command line by providing the city name and the expected weather condition as arguments. For example:
```bash
python .\weather_check_agent.py "New York" "Sunny"
```
**What Happens:**
1. The agent opens Google’s weather search for "New York".
2. It extracts the current weather condition from the page.
3. It compares the extracted condition with the expected condition ("Sunny") and prints whether they match.

## Contributing & Contact
**1. Contributing**
Contributions are welcome! If you have suggestions, improvements, or bug fixes, please fork the repository and submit a pull request.

**2. Contact**
For questions or suggestions, please send an email on ruchir.kulkarni@calfus.com
