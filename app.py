# import web scraping library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException,
)
import time
import gspread  # Gspread to access google sheets


options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
DRIVER_PATH = r"chromedriver"
options.binary_location = (
    r"/Applications/Google Chrome 3.app/Contents/MacOS/Google Chrome"
)
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
url = "https://www.grubhub.com/restaurant/cast-iron-waffles-9604-longstone-ln-charlotte/1444707"  # URL
driver.get(url)
time.sleep(10)

# Open google sheet
gc = gspread.service_account(filename="./service_account.json")
sh = gc.open("GrubHub Menu")
worksheet = sh.sheet1
worksheet.append_row(
    values=["TYPE", "NAME", "DESCRIPTION", "PRICE"]
)  # Append first header row

# scraping
categories = driver.find_elements_by_class_name("menuSection.navSection.undefined")
item_name_selector = "menuItemNew-name"
item_price_selector = "menuItem-displayPrice"
item_description_selector = "u-text-secondary.menuItemNew-description--truncate"

# Loop through each category
for category in categories:
    sectionName = category.find_element_by_class_name(
        "menuSection-headerTitle.u-flex.u-flex-justify-xs--between"
    ).text
    sectionDescription = category.find_element_by_class_name(
        "menuSection-desc.body.u-text-secondary"
    ).text
    sectionList = ["Category", sectionName, sectionDescription]
    worksheet.append_row(
        values=sectionList
    )  # append Category Names and description to worksheet

    # Loop through the items in each category
    menuItems = category.find_elements_by_class_name(
        "menuItem.u-background--tinted.u-clickable.u-inset-1 "
    )
    for i, menuItem in enumerate(menuItems):
        items = category.find_elements_by_class_name(
            "menuItem.u-background--tinted.u-clickable.u-inset-1 "
        )
        itemName = items[i].find_element_by_class_name(item_name_selector).text
        itemPrice = items[i].find_element_by_class_name(item_price_selector).text
        itemDescription = (
            items[i].find_element_by_class_name(item_description_selector).text
        )
        itemList = ["Item", itemName, itemDescription, itemPrice]
        worksheet.append_row(
            values=itemList
        )  # append Item names, description and price

        # Click each item to open modal
        items[i].click()
        time.sleep(8)

        # Check if each item modal has options, else continue
        try:
            options = driver.find_elements_by_class_name(
                "menuItemModal-choice-option-description"
            )
            if options:
                for option in options:
                    option = option.text
                    # Separate name from price in each option
                    if '+' in option:
                        name = option.split('+')[0]
                        price = option.split('+')[1]
                        optionList = ["Option", name, " ", price]
                    else:
                        optionList = ["Option", option]
                    worksheet.append_row(values=optionList)
        except NoSuchElementException:
            pass

        # Close Modal
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[at-close-add-item-modal="true"]')
            )
        ).click()
        time.sleep(8)