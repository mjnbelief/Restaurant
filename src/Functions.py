import os
import platform
from Menu import MenuOption
import json
import consolemenu as CM
from borders import frame

######################
screen = CM.Screen()

selected_language = {}
menu_items: list[MenuOption] = []

def lang(text) -> str:
    try: 
        return selected_language[text]
    except:
        return f"[{text}]"

#Convert Json file to MenuOption Object
def JosnToMenuOption(json) -> list[MenuOption]:
    menu_items = []
    for i in json:
        menu_items.append(MenuOption(**i))
    return menu_items

def GetMenu():
    with open(r".\Include\strings\Menu.json") as menu_json:
        menu = json.load(menu_json)
    return JosnToMenuOption(menu)

# Get item and added to the card
def GetBySelectedItemText(text: str):
        item = str.strip(text[0:-5]) # remove price and spaces from text
        matches = next(x for x in menu_items if x.Item == item)

        while matches.Quantity < 1:
            txt_count = CM.PromptUtils(screen).input(f"{lang("Quantity")}: ")
            if txt_count.input_string.isdigit() and int(txt_count.input_string) > 0:
                matches.Quantity = int(txt_count.input_string)
                matches.IsSelected = True
                #notify

        ShowCart()


def ShowCart():
    ClearTerminal()
    Cart = [x for x in menu_items if x.IsSelected == True] 
    
    cart_view = [(f"{lang("MyOrders")}","88;173;197","center"),("")]
    if len(Cart) > 0:
        cart_view.append((f"Name{25 * " "}Price\tQuantity","234;91;37"))
        for item in Cart:
            cart_view.append(f"{Cart.index(item) + 1} - "  + item.CartView)
        cart_view.append("")
        cart_view.append((lang("DeleteNote"),"234;91;37"))
    else:
        cart_view.append((lang("EmptyCart"),"234;91;37"))

    PrintFrame(cart_view)
    txt_delete = CM.PromptUtils(screen).input(f"{lang("EnterToContinue")}")

    if str.isdigit(txt_delete.input_string):
        try:
            cart_item = Cart.pop(int(txt_delete.input_string) - 1)
            cart_item.Unselect()
        except:
            #notify
            print("sad")

        ShowCart()


# Print with border
def PrintFrame(text):
    frame(text, 
          colour=37, 
          text_background=0, 
          frame_colour=None, 
          frame_background=None, 
          frame_style="single", 
          alignment="left", 
          display="left", 
          spacing=2,
          min_width=80,
          max_width=80, 
          window="print")

#Call the platform specific function to clear the terminal: cls on windows, reset otherwise
def ClearTerminal():
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('reset')
        