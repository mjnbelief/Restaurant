from Functions import *
import Functions as fun
from ConsoleMenuCostumize import *

def main():
    fun.selected_language = SelectLanguage()
    
    fun.menu_items = GetMenu()

    ShowMenu(fun.menu_items)

if __name__ == '__main__':
    main()