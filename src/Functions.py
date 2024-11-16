from Menu import MenuOption
# import consolemenu as CM
# from consolemenu import *
# from consolemenu.items import *
from ConsoleMenuCostumize import *
import json

#Convert Json file to MenuOption Object
def JosnToMenuOption(json) -> list[MenuOption]:
    menu_items = []
    for i in json:
        menu_items.append(MenuOption(**i))
    return menu_items

def GetMenu():
    with open(r".\Include\strings\Menu.json") as menu_json:
        menu = json.load(menu_json)
    a =  JosnToMenuOption(menu)
    return a

def ShowMenu():
    menu_items = GetMenu()

    pizzas = []
    pastas = []
    desserts = []
    trinks = []

    for item in menu_items:
        if item.Category == "Pizza":
            pizzas.append(str(item))
        elif item.Category == "Pasta":
            pastas.append(str(item))
        elif item.Category == "Dessert":
            desserts.append(str(item))
        elif item.Category == "Trink":
            trinks.append(str(item))

    console_menu = ConsoleMenu("Menu", "Welcome to ReDI food")

    submenu_pizza = SubmenuItemCustom("Pizza", SelectionMenu(pizzas, "Pizza"), console_menu)
    submenu_pasta = SubmenuItemCustom("Pasta", SelectionMenu(pastas, "Pasta"), console_menu)
    submenu_dessert = SubmenuItemCustom("Dessert", SelectionMenu(desserts, "Dessert"), console_menu)
    submenu_trink = SubmenuItemCustom("Trink", SelectionMenu(trinks, "Trink"), console_menu)

    console_menu.append_item(submenu_pizza)
    console_menu.append_item(submenu_pasta)
    console_menu.append_item(submenu_dessert)
    console_menu.append_item(submenu_trink)

    console_menu.show()
