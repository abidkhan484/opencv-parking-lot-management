from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep

def get_current_data_using_headless_browser():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Update the URL accordingly
    url = "http://localhost:5000"
    driver.get(url=url)

    sleep(2)

    occupied = driver.find_element(By.ID, "occupied").text
    available = driver.find_element(By.ID, "available").text

    driver.quit()
    return {'occupied': str(occupied), 'available': str(available)}
