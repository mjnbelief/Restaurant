from Menu import MenuOption
import json
import consolemenu as CM
from GeneralFunctions import *

screen = CM.Screen()

selected_language = {}
menu_items: list[MenuOption] = []

def SelectLanguage():
    # Select Language
    lang_path = ""
    while lang_path == "":
        PrintFrame(["Please choose your language:","1 - English","2 - Deutsch"])
        lang = input(">> ")
        
        if lang == "1":
            lang_path = r".\Include\strings\EN.json"
        elif lang == "2":
            lang_path = r".\Include\strings\DE.json"

    # Import language pack 
    try:
        with open(lang_path, encoding="UTF-8") as json_file:
            return json.load(json_file)

        ClearTerminal()
    except OSError:
        PrintFrame(["Language file not found!","Please try again."])

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
            ShowCart(with_action= False)
            txt_count = CM.PromptUtils(screen).input(f"{lang("DesiredQuantity")}: ")
            if txt_count.input_string.isdigit() and int(txt_count.input_string) > 0:
                matches.Quantity = int(txt_count.input_string)
                matches.IsSelected = True
                ShowCart()

def CalculateTotalPrice(cart:list[MenuOption]):
    total_price = 0.0
    for item in cart:
        total_price += item.Quantity * float(item.Price)

    return f"{lang("TotalPrice")}: {PriceView(total_price)}"

def ShowCart(with_action:bool = True):
    ClearTerminal()
    Cart = [x for x in menu_items if x.IsSelected == True] 
    
    cart_view = [(f"{lang("MyOrders")}","88;173;197","center"),("")]
    if len(Cart) > 0:
        cart_view.append((f"Name{25 * " "}Price\t\tQuantity","234;91;37"))
        for item in Cart:
            cart_view.append(f"{Cart.index(item) + 1} - "  + item.CartView)
        cart_view.append((CalculateTotalPrice(Cart),"88;173;197","center"))
        cart_view.append("")
        
        if with_action:
            cart_view.append((lang("CheckoutNote"),"88;173;197"))
            cart_view.append((lang("DeleteNote"),"234;91;37"))
    else:
        cart_view.append((lang("EmptyCart"),"234;91;37"))

    PrintFrame(cart_view)
    if with_action:
        txt_delete = CM.PromptUtils(screen).input(f"{lang("EnterToContinue")}")

        if str.isdigit(txt_delete.input_string) and txt_delete.input_string != "0":
            try:
                cart_item = Cart.pop(int(txt_delete.input_string) - 1)
                cart_item.Unselect()
            except:
                print(lang("ErrorOccurred"))

            ShowCart()
        elif str.isdigit(txt_delete.input_string) and txt_delete.input_string == "0":
            checkout_confirmation = CM.PromptUtils(screen).prompt_for_yes_or_no(f"{lang("CheckoutConfirmation")}")
            if checkout_confirmation: 
                Checkout()
                
def Checkout():
    PrintFrame("Viel Glück")