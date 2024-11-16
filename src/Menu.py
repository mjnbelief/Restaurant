class MenuOption:
    def __init__(self, ID, Item, Price, Category, Description):
        self.ID = ID
        self.Item = Item
        self.Price = Price
        self.Category = Category
        self.Description = Description
    
    def __repr__(self) -> str:
        spaces = 25 - len(self.Item)
        return f"{self.Item}{spaces * " "}{self.Price}"


 