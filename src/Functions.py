import json, random, datetime, threading
from pathlib import Path
import consolemenu as CM
from xhtml2pdf import pisa
from Menu import MenuOption
from bs4 import BeautifulSoup
from GeneralFunctions import *


screen = CM.Screen()

redi_console_menu: CM.ConsoleMenu
selected_language = {}
menu_items: list[MenuOption] = []

project_path = Path.cwd()

def SelectLanguage() -> dict:
    """ 
        This function allows the user to select their preferred language. 
        Based on the user's input, it loads the corresponding language file and integrates it into the program.

        Returns:
            dict: a dictionary containing the content or translations for the chosen language.
    """
    lang_path = ""
    
    while lang_path == "":
        PrintFrame(["Please choose your language:","1 - English","2 - Deutsch"])
        lang = input(">> ")
        
        if lang == "1":
            lang_path = project_path.joinpath("Include", "strings", "EN.json")
        elif lang == "2":
            lang_path = project_path.joinpath("Include", "strings", "DE.json")

    # Import language file 
    try:
        with open(str(lang_path), encoding="UTF-8") as json_file:
            return json.load(json_file)

        ClearTerminal()
    except OSError:
        logger.error("Language file not found!")
        raise PrintFrame(["Language file not found!","Please try again."])

def lang(key: str) -> str:
    """ 
        retrieves the value associated with a given key from the language dictionary and returns it.
        
        Args:
            key (str): a key of language json file 

        Returns:
            str: value of the key based on selected language.
    """
    try: 
        return selected_language[key]
    except Exception as ex:
        logger.warning(f"there is no [{key}] in language files\n{ex.args[0]}")
        return f"[{key}]"

#Convert Json file to MenuOption Object
def JosnToMenuOption(menu_item_list : list) -> list[MenuOption]:
    """ 
        Convert list of menu items to list of MenuOption 
        
        Args:
            json (list): list of json

        Returns:
            list: list of MenuOption
    """
    menu_items = []
    for item in menu_item_list:
        try:
            menu_items.append(MenuOption(**item))
        except Exception as ex:
            logger.warning(f"can not convert [{item}] to MenuOption class\n{ex.args[0]}")

    return menu_items

def GetMenu() -> list[MenuOption]:
    """ 
        open menu.json and convert to a list of MenuOption

        Returns:
            list: list of MenuOption
    """
    menu_path = project_path.joinpath("Include", "strings", "Menu.json")
    try:
        with open(str(menu_path), encoding="UTF-8") as menu_json:
            menu = json.load(menu_json)
    except OSError:
        logger.error(f"can not open Menu.json\n{OSError.strerror}")

    return JosnToMenuOption(menu)

def SetQuantity(item: MenuOption):
    """ 
        ask user to Set Quantity and then show the cart
        
        Args:
            item (MenuOption): The item that quantity should be set

    """
    try:
        while item.Quantity < 1:
            ShowCart(with_action= False)
            txt_count = CM.PromptUtils(screen).input(f"{lang("DesiredQuantity")}: ")
            if txt_count.input_string.isdigit() and int(txt_count.input_string) > 0:
                item.Quantity = int(txt_count.input_string)
                item.IsSelected = True
    except Exception as ex:
        logger.warning(f"Quantity can not set for {item}\n{ex.args[0]}")

    ShowCart()

def CalculateTotalPrice(cart:list[MenuOption]) -> float:
    """ 
        calculate total price from cart
        
        Args:
            cart (list): list of menu option that user selected them 

        Returns:
            float: total price
    """
    total_price = 0.0
    try:
        for item in cart:
            total_price += item.Quantity * float(item.Price)
    except Exception as ex:
        logger.error(f"Can not calculate total price\n{ex.args[0]}")


    return total_price

def ShowCart(with_action:bool = True):
    """ 
        show the cart (user selected items) as a table / show a message if cart is empty 
        
        Args:
            with_action (bool): allow to user to remove or checkout the items 

    """
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
            except Exception as ex:
                logger.error(f"Can not remove item from the cart\n{ex.args[0]}")

        elif txt_delete.input_string.lower() == "c":
            checkout_confirmation = CM.PromptUtils(screen).prompt_for_yes_or_no(f"{lang("CheckoutConfirmation")}")
            if checkout_confirmation: 
                Checkout(Cart)

def GenerateReceipt(cart: list[MenuOption]) -> str:
    """ 
        Generate receipt as a pdf file 
        
        Args:
            cart (list): list of menu option that user selected them 

        Returns:
            str: receipt path
    """
    receipt_html = BeautifulSoup("", "html.parser")
    try:
        receipt_html_path = project_path.joinpath("Include", "templates", "Receipt.html")
        
        with open(str(receipt_html_path),  encoding="UTF-8") as receipt_template:
            receipt_html = BeautifulSoup(receipt_template, "html.parser")
    
            date_time = datetime.datetime.now()

            # find html element by id and change the text (default: enlish)  
            if lang("Language") == "German":
                receipt_html.find("b", {"id": "Delicacies"}).string = lang("DelicaciesText")
                receipt_html.find("h3", {"id": "Authentic"}).string = lang("AuthenticText")
                receipt_html.find("th", {"id": "Quantity"}).string = lang("Quantity")
                receipt_html.find("th", {"id": "UnitPrice"}).string = lang("UnitPrice")
                receipt_html.find("th", {"id": "Price"}).string = lang("Price")
                receipt_html.find("td", {"id": "TotalPriceText"}).string = lang("TotalPrice")
                receipt_html.find("td", {"id": "TaxText"}).string = f"{lang("Tax")} (19%)"
                receipt_html.find("td", {"id": "NetPriceText"}).string = lang("NetPrice")
                receipt_html.find("h3", {"id": "EatText"}).string = lang("EatText")

            # find html element by id and change the values 
            receipt_No = receipt_html.find("span", {"id": "ReceiptNo"})
            date = receipt_html.find("span", {"id": "Date"})
            time = receipt_html.find("span", {"id": "Time"})
            total_price = receipt_html.find("td", {"id": "TotalPrice"})
            tax = receipt_html.find("td", {"id": "Tax"})
            net_price = receipt_html.find("td", {"id": "NetPrice"})
            receipt_No.string = f"RR_{date_time.strftime("%M%S")}{random.randrange(100, 999)}" #example: RR_2345109
            date.string = date_time.strftime("%d-%b-%y") # 31-Dec-24
            time.string = date_time.strftime("%X") # 23:59:59

            # add cart items to pdf table
            rows = receipt_html.find("tbody", {"id": "Items"})
            for item in cart:
                html_table_row = f"<tr><td class=\"left\">{item.Item}</td><td>{item.Quantity}</td><td>{PriceView(float(item.Price))}</td><td>{PriceView(float(item.Price) * item.Quantity)}</td></tr>"
                rows.append(BeautifulSoup(html_table_row, "html.parser"))

            #calculate prices
            total = CalculateTotalPrice(cart)
            tax_price = (19 * total) / 100.0
            total_price.string = PriceView(total)
            tax.string = PriceView(tax_price)
            net_price.string = PriceView(tax_price + total)

        # save pdf at Receipts path
        receipt_path = project_path.joinpath("Receipts", f"Receipt_{receipt_No.string}.pdf")
        with open(str(receipt_path), "wb") as pdf_file:
            pisa.CreatePDF(receipt_html.prettify(), dest=pdf_file)
    
    except OSError:
        logger.error("Can not open receipt template file")
    except Exception as ex:
        logger.error(f"can not generate receipt\n{ex.args[0]}")

    return str(receipt_path)

def Checkout(Cart: list[MenuOption]):
    """ 
        call GenerateReceipt, open Receipt pdf, then unselect user items and then start again menu after 5 sec
        
        Args:
            cart (list): list of menu option that user selected them 

    """
    redi_console_menu.pause()

    receipt_path = GenerateReceipt(Cart)

    OpenFile(receipt_path)

    for item in menu_items:
        item.Unselect()

    threading.Timer(5.0, redi_console_menu.resume).start()