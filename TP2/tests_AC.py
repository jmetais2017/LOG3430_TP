import unittest
import unittest.mock
import os
import generators 

class TestGraphAC(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple(self):

        for nbVertices in range(1, 10):
            for nbEdges in range(1, nbVertices):
                graph = generators.simple(nbVertices, nbEdges)
                self.assertEqual(graph.V(), nbVertices)
                self.assertEqual(graph.E(), nbEdges)


        pass

    def test_simple_with_probability(self):
        pass

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