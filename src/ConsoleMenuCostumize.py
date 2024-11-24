from collections.abc import Callable
import threading
from Functions import *
import Functions as fun
from consolemenu import *
from consolemenu.items import *
import consolemenu as CM
from itertools import groupby

class SubmenuItemCustom(SubmenuItem):
    def __init__(self, text: str | Callable[[], str], submenu: CM.ConsoleMenu, menu: CM.ConsoleMenu | None = None, should_exit: bool = False, menu_char: str | None = None) -> None:
        super().__init__(text, submenu, menu, should_exit, menu_char)
        
    def remove_epilogue_text(self):
            self.menu.epilogue_text = None
            
    def get_return(self):
        if self.submenu.returned_value != None:
            selected_item = self.submenu.selected_item.text
            if selected_item.Quantity > 0:
                self.menu.epilogue_text = f"*'{selected_item.Item}' {lang("DublicateItem")}" # write duplicate message at the footer of menu
            else: 
                SetQuantity(selected_item)
            threading.Timer(3.0, self.remove_epilogue_text).start() # show a duplicate message to user for 3 sec
        return self.menu.returned_value

def ShowMenu(menu_items: list[MenuOption]):
    """ 
    The main menu of all menu items that user can select and add them to cart, 
    the main menu generate by [ConsoleMenu] library,
    it has a tree structure, parent(Category) and child (items)

    Args:
        menu_items: list of all availible items
    
    Returns:
        start console menu library and show a menu of items

    """
    try:
        fun.redi_console_menu = ConsoleMenu(lang("Menu"), lang("Welcome"),show_exit_option= False)

        # Group by Category -> (Category name:string, menu items:list[MenuOption])
        grouped_by_Category = [(k, list(g)) for k, g in groupby(menu_items, lambda x: x.Category)]
        
        for group in grouped_by_Category:
            pizzas = group[1]
            submenu_pizza = SubmenuItemCustom(lang(group[0]), 
                                            SelectionMenu(pizzas, lang(group[0]), exit_option_text=lang("ReturnToMain")), 
                                            fun.redi_console_menu)
            fun.redi_console_menu.append_item(submenu_pizza)

        # add a option to parents to show cart
        fun.redi_console_menu.append_item(FunctionItem(lang("MyOrders"), ShowCart))

        fun.redi_console_menu.show()
        
    except Exception as ex:
        logger.error(f"can not run console menu and generate menu\n{ex.args[0]}")
