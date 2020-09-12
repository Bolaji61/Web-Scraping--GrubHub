#web scraping library
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
# options.add_argument('--disable-gpu')
DRIVER_PATH = r"chromedriver"
options.binary_location = r"/Applications/Google Chrome 3.app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
time.sleep(3)
driver.implicitly_wait(30)
driver.maximize_window()

#gspread
import gspread

url = 'https://www.grubhub.com/restaurant/cast-iron-waffles-9604-longstone-ln-charlotte/1444707'  #URL
driver.get(url)

gc = gspread.service_account(filename="./service_account.json")
sh = gc.open("GrubHub Menu")
worksheet = sh.sheet1
worksheet.append_row(values=["TYPE", "NAME", "DESCRIPTION", "PRICE"]) #Append first header row

preorder = driver.find_element_by_css_selector('[class="ghs-preorderButton s-btn s-btn-primary"]')
preorder.click()

categories = driver.find_elements_by_class_name("menuSection.navSection.undefined")

print(categories)
for category in categories:
    print(category)
    sectionName = category.find_element_by_class_name("menuSection-headerTitle.u-flex.u-flex-justify-xs--between").text
    sectionDescription = category.find_element_by_class_name("menuSection-desc.body.u-text-secondary").text
    sectionList = ["Category", sectionName, sectionDescription]
    worksheet.append_row(values=sectionList)  #append Category Names and description

    menuItems = category.find_elements_by_class_name("menuItem.u-background--tinted.u-clickable.u-inset-1 ")
    for menuItem in menuItems:
        itemName = menuItem.find_element_by_class_name("menuItemNew-name").text
        itemPrice = menuItem.find_element_by_class_name("menuItem-displayPrice").text
        itemDescription = menuItem.find_element_by_class_name("u-text-secondary.menuItemNew-description--truncate").text
        itemList = ["Item", itemName, itemDescription, itemPrice]
        worksheet.append_row(values=itemList)   #append Item names, description and price
        
