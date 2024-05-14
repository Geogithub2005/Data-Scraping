from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from datetime import date
import os
import json
import time

# Define Chrome driver path
CHROME_DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")

# Set Chrome options
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Run Chrome in headless mode

# Initialize Chrome webdriver with options
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)


def login():
    with open('config.json') as configFile:
        credentials = json.load(configFile)
        time.sleep(2)

        # Entering the Login Button
        driver.find_element(By.XPATH,value="//a[@href='https://id.atlassian.com/login?application=trello&continue=https%3A%2F%2Ftrello.com%2Fauth%2Fatlassian%2Fcallback%3Fdisplay%3DeyJ2ZXJpZmljYXRpb25TdHJhdGVneSI6InNvZnQifQ%253D%253D&display=eyJ2ZXJpZmljYXRpb25TdHJhdGVneSI6InNvZnQifQ%3D%3D']").click()
        time.sleep(2)

        # Filling the User name 
        username=driver.find_element(By.CSS_SELECTOR,value="input[aria-describedby='username-uid2-helper']")
        username.clear()
        username.send_keys(credentials["USERNAME"])

        # Clicking the Continue button
        continue_button = driver.find_element(By.CSS_SELECTOR, "button#login-submit span.css-178ag6o")
        continue_button.click()
        time.sleep(5)
        
        # Filling the Password
        password = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-describedby='password-uid3-helper']"))
        )
        # Scroll the password input field into view
        driver.execute_script("arguments[0].scrollIntoView(true);", password)
        # Clear any existing text in the input field and enter the password
        password.clear()
        password.send_keys(credentials["PASSWORD"])
        # Simulate pressing Enter to submit the password
        password.send_keys(Keys.RETURN)

       # Clicking the Login button
        login_button = driver.find_element(By.XPATH, "//button[@id='login-submit']")
        login_button.click() 

def navigateToBoard():
    time.sleep(5)
    driver.find_element(By.XPATH,value="//div[@title='{}']/ancestor::a".format('Bot Board')).click()
    time.sleep(5)

def addTask():
    time.sleep(2)
    add_card_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='list-add-card-button']")
    add_card_button.click()
    # Locate the textarea element
    task_text_area = driver.find_element(By.CSS_SELECTOR, "[data-testid='list-card-composer-textarea']")
    # Input your text into the textarea
    task_text_area.send_keys("Selenium add My Task")
    # Locate and click the "Add card" button
    add_card_submit_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='list-card-composer-add-card-button']")
    add_card_submit_button.click()

def main():
    try:
        driver.get("https://trello.com/")
        login()  
        navigateToBoard()
        addTask()
        input("Bot operation completed. Press any key to exit...")
        driver.quit()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
