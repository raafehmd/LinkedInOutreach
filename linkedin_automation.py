# linkedin_automation.py
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import delay, solve_captcha
from dotenv import load_dotenv

load_dotenv()

def send_connection_request(profile_url, message):
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    proxy_url = os.getenv('PROXY_URL')

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    if proxy_url:
        chrome_options.add_argument(f'--proxy-server={proxy_url}')
    
    # Anti-detection flag
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Log in to LinkedIn
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        driver.find_element(By.ID, "username").send_keys(linkedin_email)
        driver.find_element(By.ID, "password").send_keys(linkedin_password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)

        # Check for captcha challenge
        if "captcha" in driver.page_source.lower():
            logging.info("Captcha detected. Attempting to solve.")
            captcha_image = driver.find_element(By.XPATH, "//img[contains(@src, 'captcha')]")
            captcha_url = captcha_image.get_attribute("src")
            captcha_solution = solve_captcha(captcha_url)
            captcha_input = driver.find_element(By.XPATH, "//input[@name='captcha']")
            captcha_input.send_keys(captcha_solution)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(3)

        # Navigate to the target profile
        driver.get(profile_url)
        time.sleep(3)

        # Locate and click the Connect button
        connect_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Connect')]")
        if not connect_buttons:
            raise Exception("Connect button not found")
        connect_buttons[0].click()
        time.sleep(2)

        # Click "Add a note" if available
        try:
            add_note_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Add a note')]")
            add_note_button.click()
            time.sleep(1)
        except Exception:
            pass

        # Enter the connection message
        textarea = driver.find_element(By.XPATH, "//textarea[@name='message']")
        textarea.send_keys(message)
        time.sleep(1)

        # Click the Send button
        send_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Send')]")
        send_button.click()
        time.sleep(2)

    finally:
        driver.quit()

    return "Connection request sent successfully"
