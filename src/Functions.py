import random
import threading
from Menu import MenuOption
import json
import consolemenu as CM
from GeneralFunctions import *
from bs4 import BeautifulSoup
import datetime
from xhtml2pdf import pisa

screen = CM.Screen()

redi_console_menu: CM.ConsoleMenu
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

def lang(text: str) -> str:
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

def SetQuantity(item: MenuOption):
        while item.Quantity < 1:
            ShowCart(with_action= False)
            txt_count = CM.PromptUtils(screen).input(f"{lang("DesiredQuantity")}: ")
            if txt_count.input_string.isdigit() and int(txt_count.input_string) > 0:
                item.Quantity = int(txt_count.input_string)
                item.IsSelected = True
        
        ShowCart()

def CalculateTotalPrice(cart:list[MenuOption]) -> float:
    total_price = 0.0
    for item in cart:
        total_price += item.Quantity * float(item.Price)

    return total_price

def ShowCart(with_action:bool = True):
    ClearTerminal()
    Cart = [x for x in menu_items if x.IsSelected == True] 
    
    cart_view = [(f"{lang("MyOrders")}","88;173;197","center"),("")] # Title of table
    if len(Cart) > 0:
        cart_view.append((f"Name{25 * " "}Price\t\tQuantity","234;91;37")) # head of table

        for item in Cart:
            cart_view.append(f"{Cart.index(item) + 1} - "  + item.CartView)

        cart_view.append((f"{lang("TotalPrice")}: {PriceView(CalculateTotalPrice(Cart))}","88;173;197","center")) # total price
        cart_view.append(("_" * 80 ,"center")) # a line
        cart_view.append("") # a empty space
        
        if with_action:
            cart_view.append((lang("CheckoutNote"),"88;173;197")) 
            cart_view.append((lang("DeleteNote"),"234;91;37"))
    else:
        cart_view.append((lang("EmptyCart"),"234;91;37")) # show a message to user if cart is empty

    PrintFrame(cart_view)

    if with_action:
        txt_delete = CM.PromptUtils(screen).input(lang("EnterToContinue"))

        if str.isdigit(txt_delete.input_string) and txt_delete.input_string != "0":
            try:
                cart_item = Cart.pop(int(txt_delete.input_string) - 1)
                cart_item.Unselect()
                ShowCart()
            except:
                return lang("ErrorOccurred")

        elif txt_delete.input_string.lower() == "c":
            checkout_confirmation = CM.PromptUtils(screen).prompt_for_yes_or_no(f"{lang("CheckoutConfirmation")}")
            if checkout_confirmation: 
                Checkout(Cart)

def GenerateReceipt(cart: list[MenuOption]):
    receipt_html = BeautifulSoup("", "html.parser")

    with open(r".\Include\templates\Receipt.html",  encoding="UTF-8") as receipt_template:
        receipt_html = BeautifulSoup(receipt_template, "html.parser")
   
        date_time = datetime.datetime.now()

        receipt_No = receipt_html.find("span", {"id": "ReceiptNo"})
        date = receipt_html.find("span", {"id": "Date"})
        time = receipt_html.find("span", {"id": "Time"})
        total_price = receipt_html.find("td", {"id": "TotalPrice"})
        tax = receipt_html.find("td", {"id": "Tax"})
        net_price = receipt_html.find("td", {"id": "NetPrice"})
        receipt_No.string = f"RR_{date_time.strftime("%M%S")}{random.randrange(100, 999)}"
        date.string = date_time.strftime("%d-%b-%y") # 31-Dec-24
        time.string = date_time.strftime("%X") # 23:59:59
        date_time.strftime("%M%S")
        rows = receipt_html.find("tbody", {"id": "Items"})
        for item in cart:
            html_table_row = f"<tr><td class=\"left\">{item.Item}</td><td>{item.Quantity}</td><td>{PriceView(float(item.Price))}</td><td>{PriceView(float(item.Price) * item.Quantity)}</td></tr>"
            rows.append(BeautifulSoup(html_table_row, "html.parser"))

        total = CalculateTotalPrice(cart)
        tax_price = (19 * total) / 100.0
        total_price.string = PriceView(total)
        tax.string = PriceView(tax_price)
        net_price.string = PriceView(tax_price + total)

    receipt_path = f".\\Receipts\\Receipt_{receipt_No.string}.pdf"
    with open(receipt_path, "wb") as pdf_file:
        pisa.CreatePDF(receipt_html.prettify(), dest=pdf_file)
    
    return receipt_path

def Checkout(Cart: list[MenuOption]):
    redi_console_menu.pause()

    receipt_path = GenerateReceipt(Cart)

    os.system(receipt_path)

    for item in menu_items:
        item.Unselect()

    threading.Timer(5.0, redi_console_menu.resume).start()