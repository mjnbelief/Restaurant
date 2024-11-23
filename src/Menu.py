from GeneralFunctions import *

class MenuOption:
    def __init__(self, ID, Item, Price, Category, Description):
        self.ID = ID
        self.Item = Item
        self.Price = Price
        self.Category = Category
        self.Description = Description
        self.Quantity = 0
        self.IsSelected = False
        
    def __repr__(self) -> str:
        spaces = 25 - len(self.Item)
        return f"{self.Item}{spaces * " "}{self.Price}"
    
    @property
    def CartView(self) -> str:
        spaces = 25 - len(self.Item)
        price_spaces = 11 - len(self.Price)
        return f"{self.Item}{spaces * " "}{PriceView(float(self.Price))}{price_spaces * " "}{self.Quantity}"
    
    def Unselect(self):
        self.Quantity = 0
        self.IsSelected = False