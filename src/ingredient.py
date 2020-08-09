"""
@author johannpistorius
"""

from load_json import JSON
import sys


def error_message():
    sys.exit("Could not match ingredient to list. Please try again.")


class Ingredient:
    def __init__(self, item):
        self.ingredient = item
        self.data = JSON()
        self.out = {}

    def get_ingredients_list_non_exhaustive(self):
        output_stylized = {}
        self.instantiate_output()
        for (k, v) in self.out.items():
            output_stylized[k] = v["ingredients"]
        return output_stylized

    def get_ingredients_list_exhaustive(self):
        self.instantiate_output()
        return self.out

    def instantiate_output(self):
        if not self.out:
            classname = self.get_ingredient_classname(self.ingredient)
            if classname == "":
                error_message()
            self.get_ingredients(classname)

    def get_ingredients(self, classname):
        ingredients_unvisited = []
        ingredients_visited = []
        ingredients = self.get_ingredient_child(classname)
        print(ingredients["ingredients"])
        if ingredients:
            for i in range(0, len(ingredients["ingredients"])):
                ingredients_unvisited.append(ingredients["ingredients"][i]["item"])
            self.out[classname] = ingredients
            print(self.out)
        j = 0
        while j < len(ingredients_unvisited):
            if ingredients_unvisited[j] not in ingredients_visited:
                classname = ingredients_unvisited[j]
                ingredients_visited.append(ingredients_unvisited[j])
                ingredients = self.get_ingredient_child(classname)
                if ingredients:
                    for i in range(0, len(ingredients["ingredients"])):
                        ingredients_unvisited.append(ingredients["ingredients"][i]["item"])
                    self.out[classname] = ingredients
            j += 1

    def get_ingredient_child(self, ingredient):
        obj = {}
        increment = 0
        recipe_id = []
        choice_id = 0
        valid_recipe_id = False
        for recipe in self.data.get_json_object_recipes().items():
            if len(recipe[1]["products"]) <= 1 and ingredient in recipe[1]["products"][0]["item"]:
                obj[increment] = recipe[1]["ingredients"]
                recipe_id.append(recipe[1]["className"])
                increment += 1
        if obj:
            print("Recipe for: " + ingredient)
            for k, v in obj.items():
                print("Number: " + str(k))
                print("Recipe: " + str(v))
            if len(obj) > 1:
                while not valid_recipe_id:
                    try:
                        choice_id = int(input("Type the number of the recipe you wish to use: "))
                    except ValueError:
                        continue
                    if 0 <= choice_id < len(obj):
                        valid_recipe_id = True
            return self.data.get_json_object_recipes()[recipe_id[choice_id]]
        return {}

    def get_ingredient_classname(self, product):
        classname = ""
        for items in self.data.get_json_object_items().items():
            if product.lower() in items[1]["name"].lower():
                classname = items[1]["className"]
        return classname

    def __str__(self):
        return str(self.get_ingredients_list_non_exhaustive())
