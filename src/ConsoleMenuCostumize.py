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
                self.menu.epilogue_text = f"*'{selected_item.Item}' {lang("DublicateItem")}"
            else: 
                SetQuantity(selected_item)
            threading.Timer(3.0, self.remove_epilogue_text).start()
        return self.menu.returned_value

def ShowMenu(menu_items: list[MenuOption]):

    fun.redi_console_menu = ConsoleMenu(lang("Menu"), lang("Welcome"),show_exit_option= True)

    """
        Group by Category -> (Category name:string, menu items:list[MenuOption])
    """ 
    grouped_by_Category = [(k, list(g)) for k, g in groupby(menu_items, lambda x: x.Category)]
    
    for group in grouped_by_Category:
        pizzas = group[1]
        submenu_pizza = SubmenuItemCustom(lang(group[0]), 
                                          SelectionMenu(pizzas, lang(group[0]), exit_option_text=lang("ReturnToMain")), 
                                          fun.redi_console_menu)
        fun.redi_console_menu.append_item(submenu_pizza)

    fun.redi_console_menu.append_item(FunctionItem(lang("MyOrders"),ShowCart))

    fun.redi_console_menu.start()
    fun.redi_console_menu.join()
