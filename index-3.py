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
    
def select_service_type(driver, service_type):
    try:
        service_type_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/app-dashboard/app-institutions/app-institutions/app-national-visa/div/app-national-visa-reservation-appointment/app-national-visa-reservation-appointment-page/div/div/app-national-visa-reservation-appointment-data/app-visa-reservation-appointment-form/form/div/div/app-select-control[1]/mat-form-field'))
        )
        service_type_dropdown.click()

        service_type_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//span[text()="{service_type}"]'))
        )
        service_type_option.click()
    except Exception as e:
        print(f"An error occurred while selecting service type: {e}")

def select_location(driver, location):
    try:
        location_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//mat-label[text()="Lokalizacja"]'))
        )
        location_dropdown.click()

        location_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//span[text()="{location}"]'))
        )
        location_option.click()
    except Exception as e:
        print(f"An error occurred while selecting location: {e}")


def check_date_field_availability(driver):
    try:
        date_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//mat-label[text()="Termin"]'))
        )
        date_dropdown.click()

        date_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "mat-option-text")]'))
        )
        return True  # Date field is available
    except Exception as e:
        print(f"Date field is not available: {e}")
        return False  # Date field is not available

def main():
    driver = connect_to_website()
    if not driver:
        print("Failed to connect to the website. Exiting...")
        return

    time.sleep(5)

    while True:
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

        button_xpath = '//*[@id="main-content"]/app-dashboard/app-institutions/app-institutions/app-national-visa/div/app-national-visa-reservation-appointment/app-national-visa-reservation-appointment-page/div/div/app-national-visa-reservation-appointment-captcha/app-captcha/div/div[2]/app-button-control/button'
        button_clicked = click_button(driver, button_xpath)
        if not button_clicked:
            print("Failed to click the button.")
            driver.quit()
            return

        time.sleep(5)

        # Check for the existence of either the "Odśwież" or "Dalej" button to determine the correctness of the input
        odswiez_button_xpath = '//*[@id="main-content"]/app-dashboard/app-institutions/app-institutions/app-national-visa/div/app-national-visa-reservation-appointment/app-national-visa-reservation-appointment-page/div/div/app-national-visa-reservation-appointment-captcha/app-captcha/div/div[1]/app-button-control/button'
        dalej_button_xpath = '//*[@id="main-content"]/app-dashboard/app-institutions/app-institutions/app-national-visa/div/app-national-visa-reservation-appointment/app-national-visa-reservation-appointment-page/div/div/app-national-visa-reservation-appointment-captcha/app-captcha/div/div[2]/app-button-control/button'

        time.sleep(2)
        is_input_correct = check_element_existence(driver, odswiez_button_xpath) or check_element_existence(driver, dalej_button_xpath)

        if is_input_correct:

            print("Input field content is incorrect. Refreshing...")
            time.sleep(2)
            refresh_button_xpath = '//*[@id="main-content"]/app-dashboard/app-institutions/app-institutions/app-national-visa/div/app-national-visa-reservation-appointment/app-national-visa-reservation-appointment-page/div/div/app-national-visa-reservation-appointment-captcha/app-captcha/div/div[1]/app-button-control/button'
            time.sleep(10)
            refresh_clicked = click_button(driver, refresh_button_xpath)
            if not refresh_clicked:
                print("Failed to click the refresh button.")
                driver.quit()
                return
            time.sleep(5)
            continue  # Continue the loop for rechecking input correctness
        else:
            print("Input field content is correct.")
            break  # Break the loop if input is correct
    
    # Continue with the rest of the process...
    # Fill the form
    select_service_type(driver, "Wiza krajowa (inne)")
    select_location(driver, "Algier")  # Replace "Your Location" with the actual location

    # Check date availability
    desired_date = "Your Desired Date"  # Replace "Your Desired Date" with the actual date
    date_available = check_date_field_availability(driver)
    
    if date_available:
        print(f"The date is available.")
    else:
        print(f"The date is not available or not found.")

if __name__ == "__main__":
    main()
