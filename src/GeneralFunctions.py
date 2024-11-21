import os
import platform
from borders import frame

def PriceView(price:float) -> str:
    """ Returns a price with a nicer format and euro icon at the end

    Args:
        price (float): a float number that will get nicer format

    Returns:
        str: a string of price with nicer format and euro icon at the end
    """
    return f"{round(price, 2)} €"
    
    
# Print with border
def PrintFrame(text, colour= 37, alignment= "left"):
    frame(text, 
          colour=colour, 
          text_background=0, 
          frame_colour=None, 
          frame_background=None, 
          frame_style="single", 
          alignment=alignment, 
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
        