from collections.abc import Callable
from consolemenu import *
from consolemenu.items import *
import consolemenu as CM
######################
screen = CM.Screen()

class ConsoleMenuCustom(ConsoleMenu):
    def __init__(self, title: str | Callable[[], str] | None = None, subtitle: str | Callable[[], str] | None = None, screen: CM.Screen | None = None, formatter: CM.MenuFormatBuilder | None = None, prologue_text: str | Callable[[], str] | None = None, epilogue_text: str | Callable[[], str] | None = None, clear_screen: bool = True, show_exit_option: bool = True, exit_option_text: str = "Exit", exit_menu_char: str | None = None) -> None:
        super().__init__(title, subtitle, screen, formatter, prologue_text, epilogue_text, clear_screen, show_exit_option, exit_option_text, exit_menu_char)

    def select(self):
        print('current menu option:', self.current_option)
        PromptUtils(screen).enter_to_continue()
        self.selected_option = self.current_option
        self.selected_item.set_up()
        self.selected_item.action()
        self.selected_item.clean_up()
        self.returned_value = self.selected_item.get_return()
        self.should_exit = self.selected_item.should_exit
    
    def get_input(self):
        """
        Can be overridden to change the input method.
        Called in :meth:`process_user_input()<consolemenu.ConsoleMenu.process_user_input>`

        :return: the ordinal value of a single character
        :rtype: int
        """
        return self.screen.input()

class SubmenuItemCustom(SubmenuItem):
    def __init__(self, text: str | Callable[[], str], submenu: CM.ConsoleMenu, menu: CM.ConsoleMenu | None = None, should_exit: bool = False, menu_char: str | None = None) -> None:
        super().__init__(text, submenu, menu, should_exit, menu_char)

    def get_return(self):
        print(self.menu)
        PromptUtils(screen).enter_to_continue()
        return self.menu.returned_value