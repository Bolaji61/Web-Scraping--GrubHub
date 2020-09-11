from app import menuCategory
from app import menuItems
import gspread

gc = gspread.service_account(filename="./service_account.json")
sh = gc.open("GrubHub Menu")
worksheet = sh.sheet1

#Display header row
header = ["TYPE", "NAME", "DESCRIPTION", "PRICE"]
index = 1
worksheet.insert_row(header, index)

#Call the functions defined in app.py
sectionList_ = menuCategory()
itemList_ = menuItems()

# print("all section lists",sectionList_)
for sectionList in sectionList_:
    # print("singular each section list", sectionList)
    worksheet.append_row(values=sectionList, value_input_option="RAW")
    # print("Item list second all", itemList_)
    for itemList in itemList_:
        print("pls work again", itemList)
        worksheet.append_row(values=itemList, value_input_option="RAW")
