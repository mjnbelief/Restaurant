import os
import logging
import platform
from borders import frame

logger = logging.getLogger("my_logger")
logging.basicConfig(level=logging.ERROR, filename="my_logger.log")

def PriceView(price:float) -> str:
    """ 
    Returns a price with a nicer format and euro icon at the end

    Args:
        price (float): a float number that will get nicer format

    Returns:
        str: a string of price with nicer format and euro icon at the end
    """
    try:
        return f"{round(price, 2)} €"
    except Exception as ex:
        logger.error(f"can not run price view\n{ex.args[0]}")
        return f"{price} €"

    
# Print with border
def PrintFrame(text, colour= 37, alignment= "left"):
    """ 
    The frame library is costumized.This function create a frame around the content of a list. Any item of the list is considered a new line. Items allowed are strings or tuples containing: a string with text to print, one or two values (integers or strings) for foreground and background colors of the text, one string value for the alignment of the line.

    Args:
        text (any): the text or list of text, print every text of list in a new line.
        colour: allows to change the color of the text.
            default value = 37
            allowed values: "allowed values: most color names"
                            "RGB values [0-255];[0-255];[0-255]"
                            "Hex values #[00-FF][00-FF][00-FF]"
                            "xterm color number in the format x[0-255]"
                            "and ANSI codes 0, [30-37], [90-97]"
        alignment: allows to change the alignment of the text inside the frame.
            default value = "left"
            allowed values: "left", "centre", "center", "right"

    Returns:
        Print a frame around the output or the input prompt.
    """
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

def ClearTerminal():
    """ 
    clear the terminal: cls on windows, reset otherwise
    """
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('reset')
        