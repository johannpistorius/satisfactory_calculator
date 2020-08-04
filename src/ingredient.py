"""
@author johannpistorius
"""

from load_json import JSON
import sys
import numpy as np


class Ingredient:
    def __init__(self, item):
        self.ingredient = item
        self.data = JSON()
        self.out = {}

    def get_ingredients_list(self):
        if not self.out:
            classname = self.get_ingredient_classname(self.ingredient)
            if classname == "":
                sys.exit("Could not match ingredient to list. Please try again.")
            self.get_ingredients(classname)
        return self.out

    def get_ingredients(self, classname):
        ingredients = self.get_ingredient_child(classname)
        ingredients_unvisited = []
        ingredients_visited = []
        for i in range(0, len(ingredients)):
            ingredients_unvisited.append(ingredients[i]["item"])
        j = 0
        while j < len(ingredients_unvisited):
            if ingredients_unvisited[j] not in ingredients_visited:
                classname = ingredients_unvisited[j]
                ingredients_visited.append(ingredients_unvisited[j])
                ingredients = self.get_ingredient_child(classname)
                if ingredients:
                    for i in range(0, len(ingredients)):
                        ingredients_unvisited.append(ingredients[i]["item"])
                    self.out[classname] = ingredients
            j += 1

    def get_ingredient_child(self, ingredient):
        obj = {}
        increment = 0
        recipe_id = 0
        valid_recipe_id = False
        print("Recipe for: " + ingredient)
        for recipe in self.data.get_json_object_recipes().items():
            if len(recipe[1]["products"]) <= 1 and ingredient in recipe[1]["products"][0]["item"]:
                obj[increment] = recipe[1]["ingredients"]
                increment += 1
        for k, v in obj.items():
            print("Number: " + str(k))
            print("Recipe: " + str(v))
        if len(obj) > 1:
            while not valid_recipe_id:
                recipe_id = int(input("Type the number of the recipe you wish to use: "))
                if 0 <= recipe_id < len(obj):
                    valid_recipe_id = True
        return obj.get(recipe_id)

    def get_ingredient_classname(self, product):
        classname = ""
        for items in self.data.get_json_object_items().items():
            if product.lower() in items[1]["name"].lower():
                classname = items[1]["className"]
        return classname

    def __str__(self):
        return str(self.get_ingredients_list())
