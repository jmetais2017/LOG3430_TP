import unittest
import unittest.mock
import os
import generators
import utils


def sum_bernoulli(V, p):
    sum = 0
    for x in range(V):
        if(utils.bernoulli(p)):
            sum = sum + 1
    return sum


class TestGraphAC(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


#SIMPLE

    def test_simple_valid_values(self): #Les valeurs positives telles que E <= V(V-1)/2 sont valides

        for nbVertices in range(0, 10):
            for nbEdges in range(0, (int)(nbVertices*(nbVertices-1)/2)): #On teste tous les nombres d'arêtes possibles pour le nombre de sommets choisi
                graph = generators.simple(nbVertices, nbEdges)
                self.assertEqual(graph.V(), nbVertices)
                self.assertEqual(graph.E(), nbEdges)

    def test_simple_raises_value_error_when_vertices_is_negative(self): #Un nombre de noeuds négatif doit donner une erreur :
        for nbVertices in range(-3, -1):
            self.assertRaises(ValueError, generators.simple, nbVertices, -2) #si E < 0
            self.assertRaises(ValueError, generators.simple, nbVertices, 0) #si E = 0
            self.assertRaises(ValueError, generators.simple, nbVertices, 2) #si E > 0

    def test_simple_raises_value_error_when_edge_is_negative(self): #Un nombre d'arêtes négatif doit donner une erreur :
        for nbEdges in range(-3, -1):
            self.assertRaises(ValueError, generators.simple, 10, nbEdges) #si V > 0
            self.assertRaises(ValueError, generators.simple, 0, nbEdges) #si V = 0
            self.assertRaises(ValueError, generators.simple, -10, nbEdges) #si V < 0


    def test_simple_raises_value_error_when_edges_bigger_than_possible(self): #E > V(V-1)/2 doit donner une erreur
        for nbVertices in range(1, 10):
            for nbEdges in range((int)(nbVertices*(nbVertices-1)/2) + 1, (int)(nbVertices*(nbVertices-1)/2) + 3):
                self.assertRaises(ValueError, generators.simple, nbVertices, nbEdges)


#SIMPLE_WITH_PROBABILITY

    def test_simple_with_probability_with_invalid_probability(self): #Une probabilité non définie doit donner une erreur
        #Si V >= 0
        self.assertRaises(ValueError, generators.simple_with_probability, 10, -0.01)
        self.assertRaises(ValueError, generators.simple_with_probability, 10, 1.01)

        #Si V < 0
        self.assertRaises(ValueError, generators.simple_with_probability, -10, -0.01)
        self.assertRaises(ValueError, generators.simple_with_probability, -10, 1.01)

    def test_simple_with_probability(self): #Tests de valeurs valides de probabilité
        for probability in [0.2, 0.5, 0.8, 1]:
            #Si V >= 0
            nbVertices = 10
            graph = generators.simple_with_probability(nbVertices, probability)
            self.assertEqual(graph.V(), nbVertices)
            #On vérifie que l'on a bien généré approximativement le bon nombre d'arêtes
            self.assertAlmostEqual(graph.E(), sum_bernoulli((int)(nbVertices*(nbVertices-1)/2), probability))

            #Si V < 0
            self.assertRaises(ValueError, generators.simple_with_probability, -nbVertices, probability)


#BIPARTITE

    def test_bipartite_raises_valueError_with_negative_values(self):
        self.assertRaises(ValueError, generators.bipartite, -10, 10, 10)
        self.assertRaises(ValueError, generators.bipartite, 10, -10, 10)
        self.assertRaises(ValueError, generators.bipartite, 10, 10, -10)
        self.assertRaises(ValueError, generators.bipartite, -10, -10, 10)
        self.assertRaises(ValueError, generators.bipartite, -10, -10, -10)

    def test_bipartite_raises_valueError_when_too_much_edges(self):
        for v1 in range(1,3):
            for v2 in range(1,3):
                for e in range(v1 * v2 + 1, v1 * v2 + 3):
                    self.assertRaises(ValueError, generators.bipartite, v1, v2, e)

    def test_bipartite(self):
        for v1 in range(1,3):
            for v2 in range(1,3):
                for e in range(1, v1 * v2):
                    graph = generators.bipartite(v1, v2, e)
                    self.assertEqual(graph.V(), v1+v2)
                    self.assertEqual(graph.E(), e)

                    vertices1 = []
                    vertices2 = []

                    edges = graph.edges()

                    firstSet = list(edges[0])

                    vertices1.append(firstSet[0])
                    vertices2.append(firstSet[1])

                    for edge in edges:
                        asList = list(edge)

                        if(vertices1.count(asList[0]) > 0):

                            self.assertEqual(vertices1.count(asList[1]), 0)

                            if(vertices2.count(asList[1]) == 0):
                                vertices2.append(asList[1])

                        elif(vertices2.count(asList[0]) > 0):

                            self.assertEqual(vertices2.count(asList[1]), 0)

                            if(vertices1.count(asList[1]) == 0):
                                vertices1.append(asList[1])


#BIPARTITE_WITH_PROBABILITY

    def test_bipartite_with_probability_with_invalid_probability(self):
        for nbVertices in range(0, 5):
            self.assertRaises(ValueError, generators.bipartite_with_probability, 0, 0, -0.01)
            self.assertRaises(ValueError, generators.bipartite_with_probability, 0, 0, 1.01)

    def test_bipartite_with_probability(self):
        for v1 in range(4,6):
            for v2 in range(4,6):
                for probability in [0.2, 0.5, 0.8, 1]:
                    graph = generators.bipartite_with_probability(v1, v2, probability)
                    self.assertEqual(graph.V(), v1+v2)
                    self.assertAlmostEqual(graph.E(), sum_bernoulli(v1*v2, probability))

                    vertices1 = []
                    vertices2 = []

                    edges = graph.edges()

                    firstSet = list(edges[0])

                    vertices1.append(firstSet[0])
                    vertices2.append(firstSet[1])

                    for edge in edges:
                        asList = list(edge)

                        if(vertices1.count(asList[0]) > 0):

                            self.assertEqual(vertices1.count(asList[1]), 0)

                            if(vertices2.count(asList[1]) == 0):
                                vertices2.append(asList[1])

                        elif(vertices2.count(asList[0]) > 0):

                            self.assertEqual(vertices2.count(asList[1]), 0)

                            if(vertices1.count(asList[1]) == 0):
                                vertices1.append(asList[1])


#EULERIAN_CYCLE
    def test_eulerian_cycle_when_v_is_zero_or_negative_must_raise_valueError(self):
        self.assertRaises(ValueError, generators.eulerianCycle, 0, 10)
        self.assertRaises(ValueError, generators.eulerianCycle, -10, 10)

    def test_eulerian_cycle_when_e_is_negative_must_raise_valueError(self):
        self.assertRaises(ValueError, generators.eulerianCycle, 10, -10)
        self.assertRaises(ValueError, generators.eulerianCycle, -10, -10)

    def test_eulerian_cycle(self):
        for nbVertices in range(4, 10):
            for nbEdges in range(4, nbVertices):
                graph = generators.eulerianCycle(nbVertices, nbEdges)
                self.assertEqual(graph.V(), nbVertices)
                #self.assertEqual(graph.E(), nbEdges)


#REGULAR

    def test_regular(self):
        for nbVertices in range(3, 10):
            for nbEdges in range(0, nbVertices-1):
                if((nbVertices*nbEdges)%2==0):
                    graph = generators.eulerianPath(nbVertices, nbEdges)
                    self.assertEqual(graph.V(), nbVertices)
                    self.assertEqual(graph.E(), nbEdges * nbVertices)

if __name__ == '__main__':
    unittest.main()