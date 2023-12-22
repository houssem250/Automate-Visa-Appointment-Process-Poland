import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import easyocr
import time

def connect_to_website():
    driver = webdriver.Chrome()  # Use the appropriate webdriver for your browser
    try:
        driver.get("https://secure.e-konsulat.gov.pl/placowki/180/wiza-krajowa/wizyty/weryfikacja-obrazkowa?fbclid=IwAR36tJ9txjHWGui4r8jLuEpZfhVcUXdiAb0k03lbG6pR6iEfvBzkS3UmOWg")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//img[@alt="Weryfikacja obrazkowa" and @width="200" and @height="100"]')))
        return driver
    except Exception as e:
        print(f"An error occurred while connecting to the website: {e}")
        return None

def find_input_field(driver):
    try:
        input_field = driver.find_element(By.XPATH, '//input[@aria-label="Znaki z obrazka"]')
        return input_field
    except Exception as e:
        print(f"An error occurred while searching for the input field: {e}")
        return None

def capture_element_screenshot(driver, xpath):
    # Check if 'captcha.png' file exists and delete it if present
    if os.path.exists('captcha.png'):
        os.remove('captcha.png')
        print("'captcha.png' file deleted")

    try:
        element = driver.find_element_by_xpath(xpath)
        # Capture the screenshot of the specified element
        element.screenshot('captcha.png')  # Save the screenshot as 'captcha.png' in the current directory
        print("Screenshot captured and saved as 'captcha.png'")
    except Exception as e:
        print(f"An error occurred while capturing the screenshot: {e}")

def convert_image_to_text(image_path):
    try:
        # Create an EasyOCR reader object with English as the language
        reader = easyocr.Reader(['en'])
        
        # Read text from the specified image
        result = reader.readtext(image_path)
        
        # Extract and return the recognized text from the result
        if result:
            return result[0][1]
        return None
    except Exception as e:
        print(f"An error occurred during image text extraction: {e}")
        return None

def fill_input(driver, input_field, text):
    try:
        input_field.send_keys(text)
        return True
    except Exception as e:
        print(f"An error occurred while filling the input field: {e}")
        return False

# Other functions like clicking buttons, checking transitions, etc. should be implemented similarly using Selenium

def main():
    driver = connect_to_website()
    if not driver:
        print("Failed to connect to the website. Exiting...")
        return

    # Wait for the element to be present (adjust timeout as needed)
    time.sleep(5)

    input_field = find_input_field(driver)
    if not input_field:
        print("Input field not found.")
        driver.quit()
        return

    # Assume you have a function to capture the screenshot of the image
    element_xpath = '/html/body/app-root/app-home-layout/div[1]/main/div/div/app-dashboard/app-institutions/app-institutions/app-national-visa/div/app-national-visa-reservation-appointment/app-national-visa-reservation-appointment-page/div/div/app-national-visa-reservation-appointment-captcha/app-captcha/app-ultimate-captcha/div/div[2]/img'
    capture_element_screenshot(driver, element_xpath)
    # and save it to a file named 'captcha.png'
    image_path = 'captcha.png'

    # Convert the image to text using EasyOCR
    converted_text = convert_image_to_text(image_path)
    if not converted_text:
        print("Failed to convert image to text.")
        driver.quit()
        return

    # Fill the input field with the converted text
    input_filled = fill_input(driver, input_field, converted_text)
    if not input_filled:
        print("Failed to fill input field.")
        driver.quit()
        return

    # Rest of the automation flow (clicking buttons, transitions checking, etc.) should follow similarly using Selenium

    # Close the browser session after completion
    time.sleep(5)  # Just for demonstration (to see the result), remove in actual implementation
    # driver.quit()

# Execute main function
if __name__ == "__main__":
    main()
