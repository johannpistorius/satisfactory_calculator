"""
@author johannpistorius
"""

from load_json import JSON
from sympy import *


class Production:

    def __init__(self, data):
        self.data = data
        self.production = {}
        self.dict_var = {}
        self.unicode = 97

    def get_production(self, quantity_per_minute):
        matrix = Matrix([])
        classname = list(self.data.keys())[0]
        ingredients_unvisited = [classname]
        ingredients_visited = []
        increment = 0
        while increment < len(ingredients_unvisited):
            if ingredients_unvisited[increment] not in ingredients_visited:
                classname = ingredients_unvisited[increment]
                if classname not in self.dict_var:
                    self.add_var_to_dict(classname)
                if classname in self.data:
                    for j in range(0, len(self.data[classname]["ingredients"])):
                        ingredients_unvisited.append(self.data[classname]["ingredients"][j]["item"])
                    if increment == 0:
                        input_equation = self.dict_var[classname] * self.calculate_product_amount_per_minute(classname, self.data[classname]["producedIn"][0], self.data[classname]["products"][0]["amount"])
                        output_equation = int(quantity_per_minute)
                    else:
                        input_equation = self.build_input_equation(classname)
                        output_equation = self.build_output_equation(classname, self.dict_var[classname])

                else:
                    # Ore case
                    input_equation = self.build_input_equation(classname)
                    output_equation = self.dict_var[classname]
                row_equation = self.build_row_equation(input_equation, output_equation)
                matrix = matrix.row_insert(0, Matrix([[row_equation]]))
                ingredients_visited.append(classname)
            increment += 1
        print(matrix)
        print(self.dict_var)
        self.production = solve(matrix)
        return self.production
        # might need to update the styling of solution

    def add_var_to_dict(self, classname):
        var_name = chr(self.unicode)
        var_name = symbols(var_name)
        self.dict_var[classname] = var_name
        self.unicode += 1


    def build_input_equation(self, classname):
        eq = 0
        for (k, v) in self.data.items():
            for i in range(0, len(v["ingredients"])):
                if classname in v["ingredients"][i]["item"]:
                    if k not in self.dict_var:
                        self.add_var_to_dict(k)
                    eq = Add(eq, Mul(self.dict_var[k], self.calculate_product_amount_per_minute(k, self.data[k]["producedIn"][0], self.data[k]["ingredients"][i]["amount"])))
        return eq

    def build_output_equation(self, classname, var):
        return Mul(var, self.calculate_product_amount_per_minute(classname, self.data[classname]["producedIn"][0], self.data[classname]["products"][0]["amount"]))

    def build_row_equation(self, input, output):
        return Add(output, Mul(input, -1))

    def calculate_product_amount_building(self, classname, building, amount, quantity_per_minute, overclock=100):
        return quantity_per_minute / self.calculate_product_amount_per_minute(classname, building, amount)

    def calculate_product_amount_per_minute(self, classname, building, amount, overclock=100):
        recipe_time = self.calculate_building_recipe_production_time(classname, building, overclock)
        return (60 / (self.data[classname]["time"] * (recipe_time / self.data[classname]["time"]))) * amount

    def calculate_building_recipe_production_time(self, classname, building, overclock=100):
        default_clock = 100
        manufacturing_speed = JSON().get_json_object_buildings()[building]["metadata"]["manufacturingSpeed"]
        return (default_clock / overclock) * self.data[classname]["time"] * (1 / (manufacturing_speed or 1))

    def get_power_consumption(self):
        total_power_consumption = 0
        for (k, v) in self.dict_var.items():
            if k in self.data:
                total_power_consumption = total_power_consumption + self.get_building_power_consumption(self.production[v], self.data[k]["producedIn"][0])
        return total_power_consumption

    def get_building_power_consumption(self, num, building, overclock=100):
        default_power_production_exponent = 1.6
        buildings_info = JSON().get_json_object_buildings()
        power_consumption = buildings_info[building]["metadata"]["powerConsumption"]
        power_consumption_exponent = buildings_info[building]["metadata"]["powerConsumptionExponent"]
        return Mul(num, Mul(Pow(overclock/100, power_consumption_exponent or default_power_production_exponent), power_consumption or 0))
