#!/usr/bin/env python
# coding: utf-8


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from time import sleep
import os
from datetime import datetime
from config import *
from random import randint
import csv

#stop program
class InterruptExecution (Exception):
    pass

def stop():
    raise (InterruptExecution("Stopping asin collection"))
# Wait for any element to get loaded
# BY TAG
def wfe_by_tag(driver, el_tag):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, el_tag))
        )
        return element
    except Exception as e:
        return "element not found"


# BY NAME
def wfe_by_name(driver, el_name):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, el_name))
        )
        return element
    except Exception as e:
        return "element not found"


# BY ID
def wfe_by_id(driver, el_id):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, el_id))
        )
        return element
    except Exception as e:
        return "element not found"


# BY XPATH
def wfe_by_xpath(driver, el_xpath):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, el_xpath))
        )
        return element
    except Exception as e:
        return "element not found"


# BY CLASS
def wfe_by_class(driver, el_class):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, el_class))
        )
        return element
    except Exception as e:
        return "element not found"


# Scroll Down smoothly
def scroll_down(driver, page_height = None):
    if page_height is None:
        page_height = driver.execute_script("return document.body.scrollHeight")
    total_scrolled = 0
    for i in range(page_height):
        driver.execute_script(f'window.scrollBy(0,{i});')
        total_scrolled += i
        if total_scrolled >= page_height/2:
            last_no = i
            break
            
    for i in range(last_no, 0, -1):
        driver.execute_script(f'window.scrollBy(0,{i});')


# Scroll Up smoothly
def scroll_up(driver, page_height = None):
    if page_height is None:
        page_height = driver.execute_script("return document.body.scrollHeight")
    total_scrolled = 0
    for i in range(0, -page_height, -1):
        driver.execute_script(f'window.scrollBy(0,{i});')
        total_scrolled += i
        if total_scrolled <= -page_height/2:
            last_no = i
            break
    for i in range(last_no, 0):
        driver.execute_script(f'window.scrollBy(0,{i});')


# Type with manual effect
def type_slowly(element, txt):
    try:
        element.clear()
        for t in txt:
            element.send_keys(t)
            sleep(0.2)
        return True
    except:
        return False


# Collect asins
def collect_asins(driver):
    asins = []
    main_slot = driver.find_element(By.CLASS_NAME, 's-main-slot')
    prods = main_slot.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
    for prod in prods:
        try:
            asins.append(prod.get_attribute('data-asin'))
        except:
            pass
    return asins


# A few scrolls
def make_a_few_scrolls(driver):
    scroll_down(driver)
    # sleep(randint(2, 4))
    # scroll_up(driver)
    # sleep(randint(2, 4))
    # scroll_counter = randint(5, 10)
    # scrolled = 0
    # while scrolled < scroll_counter:
        # go_down = randint(0, 1)
        # if go_down == 0:
            # scroll_down(driver, randint(500, 1500))
        # else:
            # scroll_up(driver, randint(500, 1500))
        # scrolled += 1
        # sleep(2)


def generate_file_name(file_name, file_ext):
    file_no = 0
    file_name = file_name.replace(' ', '_')
    current_datetime = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    is_not_done = True
    while is_not_done:
        file_path = f"{file_name}_{current_datetime}_{file_no}.{file_ext}"
        if os.path.exists(file_path):
            file_no += 1
        else:
            is_not_done = False
            return file_path


def main(PRODUCT_NAME,ZIP_CODE):
    base_url = "https://www.amazon.com/"
    cwd = os.getcwd()




    all_asins = []
    asin_directory = f'{cwd}/data'
    if not os.path.exists(asin_directory):
        os.mkdir(asin_directory)

    file_name = generate_file_name(PRODUCT_NAME, 'csv')




    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()



    driver.get(base_url)
    sleep(3)




    # Change ZIP code
    wfe_by_id(driver, 'nav-global-location-popover-link').click()
    sleep(2)
    zip_el = wfe_by_id(driver, 'GLUXZipUpdateInput')
    sleep(2)
    type_slowly(zip_el, ZIP_CODE)
    # Apply
    driver.find_element(By.XPATH, '//input[@aria-labelledby="GLUXZipUpdate-announce"]').click()
    sleep(2)
    # Confirm
    approve_footer = wfe_by_class(driver, 'a-popover-footer')
    sleep(1)
    approve_footer.find_element(By.TAG_NAME, 'span').click()
    sleep(7)




    # Search Product
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    type_slowly(search_box, PRODUCT_NAME)
    sleep(1)
    driver.find_element(By.ID, 'nav-search-submit-button').click()
    sleep(3)
    # Select 4 Stars and up
    driver.find_element(By.XPATH, '//section[@aria-label="4 Stars & Up"]').click()
    


    try:
        # Collect all the asins
        go_next = True
        while go_next:
            make_a_few_scrolls(driver)
            # Collect asins of the page
            asins = collect_asins(driver)
            all_asins += asins
            # Go to next page
            pagination_el = driver.find_elements(By.CLASS_NAME, 'a-pagination')
            if len(pagination_el) == 1:
                next_btn = pagination_el[0].find_elements(By.PARTIAL_LINK_TEXT, 'Next')
                if len(next_btn) == 1:
                    next_btn[0].click()
                else:
                    go_next = False
        
        # Save the asins
        with open(f'{asin_directory}/{file_name}', 'w', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(['Asins'])
            for a in all_asins:
                writer.writerow([a])
    except InterruptExecution:
        # Save the asins
        with open(f'{asin_directory}/{file_name}', 'w', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(['Asins'])
            for a in all_asins:
                writer.writerow([a])




    driver.quit()

