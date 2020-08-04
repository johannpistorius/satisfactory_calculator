from unittest import TestCase

from production import Production
import numpy as np


prod = Production(5)
prod.set_matrix_a(
    np.array([[30, 15, 0, 0, 0], [20, 0, 0, -30, 0], [0, 15, -10, 0, -12], [0, 0, 40, -60, 0], [0, 0, 0, 5, -3]])
)
prod.set_matrix_b(
    np.array([[240], [0], [0], [0], [0]])
)

class TestProduction(TestCase):

    def test_build_matrix_a(self):
        self.fail()

    def test_build_matrix_b(self):
        self.fail()

    def test_get_production(self):
        np.testing.assert_allclose(prod.get_production(), np.array([[4.5], [7], [4.5], [3], [5]]))
