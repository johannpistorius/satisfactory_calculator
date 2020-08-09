"""
@author johannpistorius
"""

from ingredient import Ingredient
from production import Production
from load_json import JSON
import sys


def get_ingredients_name():
    data = JSON()
    for items in data.get_json_object_items().items():
        print(items[1]["name"])


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    try:
        command = sys.argv[1]
        if command == "help":
            if len(sys.argv) > 2:
                if sys.argv[2] == "ingredients":
                    get_ingredients_name()
            else:
                print("List of commands:\n" \
                      "-> help : get list of available commands\n" \
                      "-> help ingredients: get list of ingredients\n" \
                      "-> ingredient {ingredient name} -> get all ingredients for specified ingredient\n" \
                      "\t-> e.g. ingredient modular frame\n"\
                      "-> production {ingredient name} {amount per minute} -> get production stats\n" \
                      "\t-> e.g. production modular frame 10")
            sys.exit()
        elif command == "ingredient":
            ingredient = ""
            for i in range(2, len(sys.argv)):
                ingredient += sys.argv[i] + " "
            ingredient = ingredient.rstrip()
            print("Command: " + command + " Ingredient: " + ingredient)
            item = Ingredient(ingredient)
            print(item)
        elif command == "production":
            ingredient = ""
            quantity = ""
            for i in range(2, len(sys.argv)):
                if not represents_int(sys.argv[i]):
                    ingredient += sys.argv[i] + " "
                else:
                    quantity = sys.argv[i]
            ingredient = ingredient.rstrip()
            print("Command: " + command + " Ingredient: " + ingredient + " Quantity: " + quantity)
            item = Ingredient(ingredient)
            data = item.get_ingredients_list_exhaustive()
            prod = Production(data)
            print(prod.get_production(quantity))
            print("Power required: " + str(prod.get_power_consumption()) + " MW")
        else:
            sys.exit("Not a valid command : does not exist. See `help` for more info.")
    except IndexError:
        sys.exit("Not a valid command : missing arguments. See `help` for more info.")
