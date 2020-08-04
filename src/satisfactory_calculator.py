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


if __name__ == "__main__":
    try:
        command = sys.argv[1]
        if command == "help":
            if len(sys.argv) > 1:
                if sys.argv[2] == "ingredients":
                    get_ingredients_name()
            else:
                print("helpful commands here")
            sys.exit()
        elif command == "ingredient":
            ingredient = ""
            for i in range(2, len(sys.argv)):
                ingredient += sys.argv[i]+" "
            ingredient = ingredient.rstrip()
            print("Command: " + command + " Ingredient: " + ingredient)
            item = Ingredient(ingredient)
            print(item)
        elif command == "production":
            ingredient = sys.argv[2]
            quantity = sys.argv[3]
            print("Command: " + command + " Ingredient: " + ingredient + " Quantity: " + quantity)
            item = Ingredient(ingredient)
            data = item.get_ingredients_list()
            prod = Production(len(data["ingredients"]))
            prod.build_matrix_a(data)
            prod.build_matrix_b(data)
            prod.get_production()
        else:
            print("Not a valid command : does not exist. See `help` for more info.")
    except IndexError:
        print("Not a valid command : missing arguments. See `help` for more info.")
