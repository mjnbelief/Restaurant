import json
from Functions import *
import Functions as fun
from ConsoleMenuCostumize import *

""" Language """
def SelectLanguage():
    # Select Language
    lang_path = ""
    while lang_path == "":
        PrintFrame(["Please choose your language:","1 - English","2 - Deutsch"])
        lang = input(">> ")
        
        if lang == "1" or lang == "English":
            lang_path = r".\Include\strings\EN.json"
        elif lang == "2" or lang == "Deutsch":
            lang_path = r".\Include\strings\DE.json"

    # Import language pack 
    try:
        with open(lang_path) as json_file:
            fun.selected_language = json.load(json_file)

        ClearTerminal()
    except OSError:
        PrintFrame(["Language file not found!","Please try again."])
""" End Language """

def main():
    SelectLanguage()
    
    fun.menu_items = GetMenu()

    ShowMenu(fun.menu_items)

if __name__ == '__main__':
    main()
    