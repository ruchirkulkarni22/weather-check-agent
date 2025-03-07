"""
Weather Checker Agent

This script automates checking the weather for a specified city and validates if it matches
an expected condition. It uses Selenium to navigate to Google Weather, extract the current
weather condition, and compare it with the expected condition.

Usage:
    python weather_checker.py <city_name> <expected_condition>

Example:
    python weather_checker.py "Pune" "Sunny"
"""

import sys
import time
import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def check_weather(city, expected_condition):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Set a common user agent to avoid detection
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Add settings to bypass bot detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Determine if running on Windows and set appropriate settings
    is_windows = platform.system() == "Windows"
    
    try:
        print(f"Setting up WebDriver...")
        
        # For Windows, use a more specific installation approach
        if is_windows:
            # Get the ChromeDriver executable path
            driver_path = ChromeDriverManager().install()
            print(f"ChromeDriver installed at: {driver_path}")
            
            # Create service object
            service = Service(executable_path=driver_path)
            
            # Create driver with service
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            # For non-Windows systems, use the default approach
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
        
        # Add JavaScript to modify navigator properties to avoid detection
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        })
        
        # Navigate to Google Weather for the specified city
        url = f"https://www.google.com/search?q=weather+{city.replace(' ', '+')}"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Wait for page to load completely
        print("Waiting for page to load completely...")
        time.sleep(5)
        
        # Take an initial screenshot to see the page state
        initial_screenshot = f"{city.replace(' ', '_')}_initial.png"
        driver.save_screenshot(initial_screenshot)
        print(f"Initial page screenshot saved as {initial_screenshot}")
        
        # Try to extract weather using multiple approaches
        print("Attempting to extract weather information...")
        
        # Use known Google Weather element selectors
        weather_selectors = [
            (By.ID, "wob_dc"),
            (By.CSS_SELECTOR, ".wob_dc"),
            (By.XPATH, "//span[@id='wob_dc']"),
            (By.XPATH, "//div[@id='wob_dcp']/div"),
            (By.XPATH, "//div[@class='UQt4rd']"),
            (By.XPATH, "//div[contains(@class, 'VQF4g')]"),
            (By.XPATH, "//span[contains(@class, 'BBwThe')]"),
            (By.XPATH, "//div[contains(text(), '°')]/../div[1]"),
        ]
        
        actual_condition = None
        for selector_type, selector_value in weather_selectors:
            try:
                print(f"Trying selector: {selector_type} = {selector_value}")
                wait = WebDriverWait(driver, 3)
                element = wait.until(EC.visibility_of_element_located((selector_type, selector_value)))
                condition = element.text.strip()
                if condition and len(condition) > 0:
                    actual_condition = condition
                    print(f"Found weather condition: '{actual_condition}' using {selector_value}")
                    break
            except Exception as e:
                print(f"Selector {selector_value} failed: {str(e)[:100]}...")
        
        # Look for weather-related terms in visible text
        if not actual_condition:
            print("Trying to find weather conditions in page text...")
            try:
                # Common weather conditions to look for
                conditions = [
                    "Sunny", "Clear", "Partly cloudy", "Cloudy", "Rain", "Showers",
                    "Thunderstorm", "Snow", "Mist", "Fog", "Haze", "Smoke", "Dust",
                    "Drizzle", "Overcast"
                ]
                
                # Get all text elements on the page
                elements = driver.find_elements(By.XPATH, "//div[string-length(text()) > 2]")
                
                for element in elements:
                    text = element.text.strip()
                    # Check if any known weather condition is in this text
                    for condition in conditions:
                        if condition.lower() in text.lower():
                            actual_condition = text
                            print(f"Found likely weather text: '{actual_condition}'")
                            break
                    if actual_condition:
                        break
            except Exception as e:
                print(f"Text search approach failed: {str(e)[:100]}...")
        
        # Try to extract from page title
        if not actual_condition:
            try:
                title = driver.title
                print(f"Page title: {title}")
                if "weather" in title.lower():
                    # Google weather titles often have format "Weather Condition - Weather for City"
                    parts = title.split(" - ")
                    if len(parts) > 0:
                        actual_condition = parts[0].strip()
                        print(f"Extracted weather from title: '{actual_condition}'")
            except Exception as e:
                print(f"Title extraction failed: {str(e)[:100]}...")
        
        # Parse the page source for weather patterns
        if not actual_condition:
            try:
                print("Analyzing page source for weather information...")
                page_source = driver.page_source.lower()
                
                # Common patterns in Google's weather widget HTML
                patterns = [
                    "id=\"wob_dc\">([^<]+)<",
                    "class=\"BBwThe\">([^<]+)<",
                    "class=\"VQF4g\">([^<]+)<",
                    "data-local-attribute=\"weather-condition\">([^<]+)<"
                ]
                
                import re
                for pattern in patterns:
                    matches = re.findall(pattern, page_source)
                    if matches and len(matches) > 0:
                        actual_condition = matches[0].strip()
                        print(f"Found condition in source: '{actual_condition}'")
                        break
            except Exception as e:
                print(f"Source analysis failed: {str(e)[:100]}...")
        
        # Final result
        if actual_condition:
            print(f"Current weather in {city}: {actual_condition}")
            
            # Compare with expected condition (case-insensitive)
            is_match = expected_condition.lower() in actual_condition.lower()
            print("-" * 50)
            result_message = (
                f"✅ Weather matches your expectation!" 
                if is_match 
                else f"❌ Weather doesn't match your expectation."
            )
            print(result_message)
            print("-" * 50)
            print(f"Expected: {expected_condition}")
            print(f"Actual: {actual_condition}")
            
            # Capture a final screenshot
            screenshot_path = f"{city.replace(' ', '_')}_weather.png"
            driver.save_screenshot(screenshot_path)
            print(f"Final screenshot saved as {screenshot_path}")
            
            return is_match
        else:
            print(f"Couldn't extract weather condition for {city}.")
            print("Please check the screenshots to see what the page looks like.")
            return False
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        if 'driver' in locals():
            print("Taking error screenshot...")
            driver.save_screenshot(f"{city.replace(' ', '_')}_error.png")
        return False
    
    finally:
        # Close the browser
        if 'driver' in locals():
            driver.quit()
            print("Browser closed.")

def main():
    """
    Main function to parse command line arguments and check weather.
    """
    # Check if correct number of arguments provided
    if len(sys.argv) != 3:
        print("Usage: python weather_checker.py <city_name> <expected_condition>")
        print("Example: python weather_checker.py \"Pune\" \"Sunny\"")
        sys.exit(1)
    
    # Extract command line arguments
    city = sys.argv[1]
    expected_condition = sys.argv[2]
    
    print(f"Weather Checker Agent Started")
    print(f"Checking if the weather in {city} is {expected_condition}...")
    print("-" * 50)
    
    # Check the weather
    result = check_weather(city, expected_condition)
    
    print("-" * 50)
    print("Weather Checker Agent Completed")
    
    # Return exit code based on whether expectation was met
    sys.exit(0 if result else 1)

if __name__ == "__main__":
    main()