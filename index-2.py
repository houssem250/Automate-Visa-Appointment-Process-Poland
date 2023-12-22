import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import easyocr
import time

def connect_to_website():
    driver = webdriver.Chrome()
    try:
        driver.get("https://secure.e-konsulat.gov.pl/placowki/180/wiza-krajowa/wizyty/weryfikacja-obrazkowa?fbclid=IwAR36tJ9txjHWGui4r8jLuEpZfhVcUXdiAb0k03lbG6pR6iEfvBzkS3UmOWg")
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

def capture_element_screenshot(driver, xpath, image_path):
    try:
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"'{image_path}' file deleted")

        element = driver.find_element(By.XPATH, xpath)
        element.screenshot(image_path)
        print(f"Screenshot captured and saved as '{image_path}'")
        return True
    except Exception as e:
        print(f"An error occurred while capturing the screenshot: {e}")
        return False

def convert_image_to_text(image_path):
    try:
        reader = easyocr.Reader(['en'])
        result = reader.readtext(image_path)
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

def click_button(driver, button_xpath):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        button.click()
        return True
    except Exception as e:
        print(f"An error occurred while clicking the button: {e}")
        return False

def check_element_existence(driver, element_xpath):
    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )
        return True  # Element exists
    except:
        return False  # Element doesn't exist or not found within the timeout

def main():
    driver = connect_to_website()
    if not driver:
        print("Failed to connect to the website. Exiting...")
        return

    time.sleep(5)

    input_field = find_input_field(driver)
    if not input_field:
        print("Input field not found.")
        driver.quit()
        return

    element_xpath = '/html/body/app-root/app-home-layout/div[1]/main/div/div/app-dashboard/app-institutions/app-institutions/app-national-visa/div/app-national-visa-reservation-appointment/app-national-visa-reservation-appointment-page/div/div/app-national-visa-reservation-appointment-captcha/app-captcha/app-ultimate-captcha/div/div[2]/img'
    image_path = 'captcha.png'

    capture_success = capture_element_screenshot(driver, element_xpath, image_path)
    if not capture_success:
        print("Failed to capture the screenshot.")
        driver.quit()
        return

    converted_text = convert_image_to_text(image_path)
    if not converted_text:
        print("Failed to convert image to text.")
        driver.quit()
        return

    input_filled = fill_input(driver, input_field, converted_text)
    if not input_filled:
        print("Failed to fill input field.")
        driver.quit()
        return

    time.sleep(5)

     # Click the button for further action or refresh
    button_xpath = '//*[@id="main-content"]/app-dashboard/app-institutions/app-institutions/app-national-visa/div/app-national-visa-reservation-appointment/app-national-visa-reservation-appointment-page/div/div/app-national-visa-reservation-appointment-captcha/app-captcha/div/div[2]/app-button-control/button'
    button_clicked = click_button(driver, button_xpath)
    if not button_clicked:
        print("Failed to click the button.")
        return

    time.sleep(5)

    # Check for the existence of the image component to determine the correctness of the input
    img_existence_xpath = '//*[@id="main-content"]/app-dashboard/app-institutions/app-institutions/app-national-visa/div/app-national-visa-reservation-appointment/app-national-visa-reservation-appointment-page/div/div/app-national-visa-reservation-appointment-captcha/app-captcha/div/div[2]/img'
    is_input_correct = not check_element_existence(driver, img_existence_xpath)

    if is_input_correct:
        print("Input field content is correct.")
    else:
        print("Input field content is incorrect.")
    # driver.quit()

if __name__ == "__main__":
    main()
