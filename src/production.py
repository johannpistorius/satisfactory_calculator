"""
@author johannpistorius
"""

import numpy as np


class Production:

    def __init__(self, n):
        self.matrixA = np.zeros((n, n))
        self.matrixB = np.zeros((n, 1))

    def build_matrix_a(self, data):
        # todo
        for ingredient in data["ingredients"].items:
            current = ingredient["name"]
            amount = ingredient["output"]
            child = np.zeros(len(ingredient["input"]))
            for i in range(0, len(ingredient["input"])):
                np.put(child, ingredient["input"][i]["name"])

    def build_matrix_b(self, data):
        # todo
        print("todo")

    def set_matrix_a(self, m):
        self.matrixA = m

    def set_matrix_b(self, m):
        self.matrixB = m

    def get_production(self):
        return np.dot(np.linalg.inv(self.matrixA), self.matrixB)
