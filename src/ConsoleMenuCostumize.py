from collections.abc import Callable
from Functions import *
from consolemenu import *
from consolemenu.items import *
import consolemenu as CM

class SubmenuItemCustom(SubmenuItem):
    def __init__(self, text: str | Callable[[], str], submenu: CM.ConsoleMenu, menu: CM.ConsoleMenu | None = None, should_exit: bool = False, menu_char: str | None = None) -> None:
        super().__init__(text, submenu, menu, should_exit, menu_char)

    def get_return(self):
        if self.submenu.returned_value != None:
            GetBySelectedItemText(self.submenu.selected_item.text)
        return self.menu.returned_value

def ShowMenu(menu_items):
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
        elif item.Category == "Drink":
            trinks.append(str(item))

    console_menu = ConsoleMenu(lang("Menu"), lang("Welcome"), exit_option_text=lang("Checkout"))

    submenu_pizza = SubmenuItemCustom(lang("Pizzas"), SelectionMenu(pizzas, lang("Pizzas")), console_menu)
    submenu_pasta = SubmenuItemCustom(lang("Pastas"), SelectionMenu(pastas, lang("Pastas")), console_menu)
    submenu_dessert = SubmenuItemCustom(lang("Desserts"), SelectionMenu(desserts, lang("Desserts")), console_menu)
    submenu_trink = SubmenuItemCustom(lang("Drinks"), SelectionMenu(trinks, lang("Drinks")), console_menu)

    submenu_trink = SubmenuItemCustom(lang("Drinks"), SelectionMenu(trinks, lang("Drinks")), console_menu)

    console_menu.append_item(submenu_pizza)
    console_menu.append_item(submenu_pasta)
    console_menu.append_item(submenu_dessert)
    console_menu.append_item(submenu_trink)
    console_menu.append_item(FunctionItem("MyOrders",ShowCart))

    console_menu.show()
