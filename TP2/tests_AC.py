import unittest
import unittest.mock
import os
import generators
import utils 

def sum_bernoulli(V, p):
    sum = 0

    for x in range(0, (int)(V*(V-1)/2)):
        if(utils.bernoulli(p)):
            sum = sum + 1

    return sum

class TestGraphAC(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_valid_values(self):

        for nbVertices in range(1, 10):
            for nbEdges in range(1, (int)(nbVertices*(nbVertices-1)/2)):
                graph = generators.simple(nbVertices, nbEdges)
                self.assertEqual(graph.V(), nbVertices)
                self.assertEqual(graph.E(), nbEdges)

    def test_simple_raises_value_error_when_vertices_is_negative(self):
        for nbVertices in range(-3, -1):
            self.assertRaises(ValueError, generators.simple, nbVertices, 0)

    def test_simple_raises_value_error_when_edge_is_negative(self):
        for nbVertices in range(1, 10):
            for nbEdges in range(-3, -1):
                self.assertRaises(ValueError, generators.simple, nbVertices, nbEdges)

    def test_simple_raises_value_error_when_edges_bigger_than_possible(self):
        for nbVertices in range(1, 10):
            for nbEdges in range((int)(nbVertices*(nbVertices-1)/2) + 1, (int)(nbVertices*(nbVertices-1)/2) + 3):
                self.assertRaises(ValueError, generators.simple, nbVertices, nbEdges)

    def test_simple_with_probability_with_invalid_probability(self):
        for nbVertices in range(0, 5):
            self.assertRaises(ValueError, generators.simple_with_probability, nbVertices, -0.01)
            self.assertRaises(ValueError, generators.simple_with_probability, nbVertices, 1.01)

    def test_simple_with_probability(self):
        for nbVertices in range(10, 20):
            for probability in [0.2, 0.5, 0.8, 1]:
                graph = generators.simple_with_probability(nbVertices, probability)
                self.assertEqual(graph.V(), nbVertices)
                self.assertAlmostEqual(graph.E(), sum_bernoulli(nbVertices, probability))

    def test_bipartite(self):
        pass

    def test_bipartite_with_probability(self):
        pass

    def test_eulerian_cycle(self):
        pass

    def test_regular(self):
        pass

if __name__ == '__main__':
    unittest.main()