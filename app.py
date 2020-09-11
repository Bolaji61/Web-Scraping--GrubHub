from selenium import webdriver #Web scraping tool

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
DRIVER_PATH = r"chromedriver"
options.binary_location = r"/Applications/Google Chrome 3.app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

url = "https://www.grubhub.com/restaurant/cast-iron-waffles-9604-longstone-ln-charlotte/1444707"  #URL
driver.get(url)

def menuCategory():
    """
    Returns: A list of all categories of menu and their descriptions
    """
    categories = driver.find_elements_by_class_name("menuSection.navSection.undefined")
    # print("Categories", categories)
    sectionList_ = []
    for category in categories:
        sectionName = category.find_element_by_class_name("menuSection-headerTitle.u-flex.u-flex-justify-xs--between").text
        sectionDescription = category.find_element_by_class_name("menuSection-desc.body.u-text-secondary").text
        sectionList = [sectionName, sectionDescription]
        sectionList_.append(sectionList)
    return sectionList_

def menuItems():
    """
    Returns: A list of all sub-category menu(Items), their descriptions and prices.
    """
    menuItems = driver.find_elements_by_class_name("menuItem.u-background--tinted.u-clickable.u-inset-1 ")
    # print("Menu Items", menuItems)
    itemList_ = []
    for menuItem in menuItems:
        itemName = menuItem.find_element_by_class_name("menuItemNew-name").text
        itemPrice = menuItem.find_element_by_class_name("menuItem-displayPrice").text
        itemDescription = menuItem.find_element_by_class_name("u-text-secondary.menuItemNew-description--truncate").text
        itemList = [itemName, itemDescription, itemPrice]
        itemList_.append(itemList)
    return itemList_
