import json
import Functions
from os import system

text = {}
lang_path = ""

""" Language """
# Select Language
while lang_path == "":
    lang = input("Welcome to ReDI Restaurant!\n Please choose your language:\n 1.English\n 2.Deutsch\n")
    if lang == "1" or lang == "English":
        lang_path = r".\Include\strings\EN.json"
    elif lang == "2" or lang == "Deutsch":
        lang_path = r".\Include\strings\DE.json"

# Import language pack 
with open(lang_path) as json_file:
    text = json.load(json_file)

system('cls')  # clears stdout
""" End Language """

Functions.ShowMenu()
