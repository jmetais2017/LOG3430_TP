import unittest
import unittest.mock
import os
import generators
import utils

#fonction utilitaire permettant de calculer la somme de bernoulli
def sum_bernoulli(V, p):
    sum = 0
    for x in range(V):
        if(utils.bernoulli(p)):
            sum = sum + 1
    return sum


class TestGraphAC(unittest.TestCase):

    #on suppose que setup et teardown doivent etre presents par convention
    def setUp(self):
        pass

    def tearDown(self):
        pass


#SIMPLE

    #Les valeurs positives telles que E <= V(V-1)/2 sont valides
    def test_simple_valid_values(self):

    #On teste tous les nombres d'arêtes possibles pour le nombre de sommets choisi
        for nbVertices in range(0, 10):
            for nbEdges in range(0, nbVertices*(nbVertices-1)//2):
                graph = generators.simple(nbVertices, nbEdges)
                self.assertEqual(graph.V(), nbVertices)
                self.assertEqual(graph.E(), nbEdges)

    #Un nombre de noeuds négatif doit donner une erreur :
    def test_simple_raises_value_error_when_vertices_is_negative(self):
        for nbVertices in range(-3, -1): # V invalides
            for nbEdges in [-3, -1, 0, 3, 5]: # E valides et invalides

                #on s'assure qu'une erreur est lancée
                self.assertRaises(ValueError, generators.simple, nbVertices, nbEdges)

    #Un nombre d'arêtes négatif doit donner une erreur  peut importe la valeur de V:
    def test_simple_raises_value_error_when_edge_is_negative(self):
        for V in [10, 0, -10]: # V valides et invalides
            for nbEdges in range(-3, -1): # E invalides

                #on s'assure qu'une erreur est lancée
                self.assertRaises(ValueError, generators.simple, V, nbEdges)

    #E > V(V-1)/2 doit donner une erreur
    def test_simple_raises_value_error_when_edges_bigger_than_possible(self):
        for nbVertices in range(1, 10): # V valides
            for nbEdges in range((int)(nbVertices*(nbVertices-1)/2) + 1, (int)(nbVertices*(nbVertices-1)/2) + 3): # E trop gros

                #on s'assure qu'une erreur est lancée
                self.assertRaises(ValueError, generators.simple, nbVertices, nbEdges)


#SIMPLE_WITH_PROBABILITY

    #Une probabilité invalide ( P n'appartenant pas a [0, 1]) doit donner une erreur peut importe si V est valide ou non
    def test_simple_with_probability_with_invalid_probability(self):
        for V in [10, -10]: # V valide et invalide
            for P in [-0.01, 1.01]: # P invalides

                #on s'assure qu'une erreur est lancée
                self.assertRaises(ValueError, generators.simple_with_probability, V, P)

    #un nombre de vertices invalides doit donner une erreur peut importe si P est valide ou non
    def test_simple_with_probability_with_invalid_vertices(self):
        for V in [-3, -2, -1]: # V invalides
            for P in [-0.01, 0.2, 0.5, 0.8, 1, 1.01]: # P valides et invalides

                #on s'assure qu'une erreur est lancée
                self.assertRaises(ValueError, generators.simple_with_probability, V, P)

    #Tests de valeurs valides de probabilité
    def test_simple_with_probability(self):
        for nbVertices in range(5,8): # V valides
            for probability in [0.2, 0.5, 0.8, 1]: # P valides
                graph = generators.simple_with_probability(nbVertices, probability)
                
                #verifier nbVertices
                self.assertEqual(graph.V(), nbVertices)

                #On vérifie que l'on a bien généré approximativement le bon nombre d'arêtes à l'aide de la théorie de la probabilité
                self.assertAlmostEqual(graph.E(), sum_bernoulli((int)(nbVertices*(nbVertices-1)/2), probability))


#BIPARTITE

    #Test quand V1 est negatif peut importe V2 et E
    def test_bipartite_raises_valueError_with_negative_V1(self):
        for V1 in [-2, -1]: # V1 invalides
            for V2 in [-2, -1, 2, 3]: # V2 valdies et invalides
                for E in [-2, -1, 2, 3]: # E valides et invalides
                    self.assertRaises(ValueError, generators.bipartite, V1, V2, E)

    #Test quand V2 est negatif peut importe V1 et E
    def test_bipartite_raises_valueError_with_negative_V2(self):
        for V1 in [-2, -1, 2, 3]: # V1 valides et invalides
            for V2 in [-2, -1]: # V2invalides
                for E in [-2, -1, 2, 3]: # E valides et invalides
                    self.assertRaises(ValueError, generators.bipartite, V1, V2, E)

    #Test quand E est negatif peut importe V1 et V2
    def test_bipartite_raises_valueError_with_negative_E(self):
        for V1 in [-2, -1, 2, 3]: # V1 valides et invalides
            for V2 in [-2, -1, 2, 3]: # V2 valdies et invalides
                for E in [-2, -1]: # E invalides
                    self.assertRaises(ValueError, generators.bipartite, V1, V2, E)

    #Test quand E est trop gros peut importe V1 et V2
    def test_bipartite_raises_valueError_when_too_much_edges(self):
        for v1 in [-2, -1, 2, 3, 4]: # V1 valides et invalides
            for v2 in [-2, -1, 2, 3, 4]: # V2 valdies et invalides
                for e in range(v1 * v2 + 1, v1 * v2 + 3):
                    self.assertRaises(ValueError, generators.bipartite, v1, v2, e)

    #Test pour bipartite avec des entrees valides
    def test_bipartite(self):
        for v1 in range(1,3):
            for v2 in range(1,3):
                for e in range(1, v1 * v2):
                    graph = generators.bipartite(v1, v2, e)
                    self.assertEqual(graph.V(), v1+v2) # test V
                    self.assertEqual(graph.E(), e) # test E

                    #on va essayer d'extraire les noeuds en 2 sous-graphes bipartites
                    vertices1 = []
                    vertices2 = []

                    edges = graph.edges()

                    firstSet = list(edges[0])

                    vertices1.append(firstSet[0])
                    vertices2.append(firstSet[1])

                    for edge in edges:
                        asList = list(edge)

                        if(vertices1.count(asList[0]) > 0):
                            
                            #on s'assure les noeuds de l'arrete ne se trouvent pas dans le meme sous-ensemble
                            self.assertEqual(vertices1.count(asList[1]), 0)

                            if(vertices2.count(asList[1]) == 0):
                                vertices2.append(asList[1])

                        elif(vertices2.count(asList[0]) > 0):

                            #on s'assure les noeuds de l'arrete ne se trouvent pas dans le meme sous-ensemble
                            self.assertEqual(vertices2.count(asList[1]), 0)

                            if(vertices1.count(asList[1]) == 0):
                                vertices1.append(asList[1])


#BIPARTITE_WITH_PROBABILITY

    #Test quand V1 est negatif peut importe V2 et P
    def test_bipartite_with_probability_raises_valueError_with_negative_V1(self):
        for V1 in [-2, -1]: # V1 invalides
            for V2 in [-2, -1, 2, 3]: # V2 valides et invalides
                for P in [-0.01, 0.2, 0.5, 0.8, 1, 1.01]: # P valides et invalides
                    self.assertRaises(ValueError, generators.bipartite_with_probability, V1, V2, P)

    #Test quand V2 est negatif peut importe V1 et P
    def test_bipartite__ith_probability_raises_valueError_with_negative_V2(self):
        for V1 in [-2, -1, 2, 3]: # V1 valides et invalides
            for V2 in [-2, -1]: # V2 invalides
                for P in [-0.01, 0.2, 0.5, 0.8, 1, 1.01]: # P valides et invalides
                    self.assertRaises(ValueError, generators.bipartite_with_probability, V1, V2, P)

    #Test quand P est invalide peut importe V1 et V2
    def test_bipartite_with_probability_raises_valueError_with_invalid_P(self):
        for V1 in [-2, -1, 2, 3]: # V1 valides et invalides
            for V2 in [-2, -1, 2, 3]: # V2 valides et invalides
                for P in [-0.01, 1.01]: # P invalides
                    self.assertRaises(ValueError, generators.bipartite_with_probability, V1, V2, P)

    def test_bipartite_with_probability(self):
        for v1 in range(4,6):
            for v2 in range(4,6):
                for probability in [0.2, 0.5, 0.8, 1]:
                    graph = generators.bipartite_with_probability(v1, v2, probability)
                    self.assertEqual(graph.V(), v1+v2) # verifier V

                    #on verifie le nombre d'arrete a l'aide de la probabilite
                    self.assertAlmostEqual(graph.E(), sum_bernoulli(v1*v2, probability))

                    #on va essayer d'extraire les noeuds en 2 sous-graphes bipartites
                    vertices1 = []
                    vertices2 = []

                    edges = graph.edges()

                    firstSet = list(edges[0])

                    vertices1.append(firstSet[0])
                    vertices2.append(firstSet[1])

                    for edge in edges:
                        asList = list(edge)

                        if(vertices1.count(asList[0]) > 0):
                            
                            #on s'assure les noeuds de l'arrete ne se trouvent pas dans le meme sous-ensemble
                            self.assertEqual(vertices1.count(asList[1]), 0)

                            if(vertices2.count(asList[1]) == 0):
                                vertices2.append(asList[1])

                        elif(vertices2.count(asList[0]) > 0):

                            #on s'assure les noeuds de l'arrete ne se trouvent pas dans le meme sous-ensemble
                            self.assertEqual(vertices2.count(asList[1]), 0)

                            if(vertices1.count(asList[1]) == 0):
                                vertices1.append(asList[1])

#EULERIAN_CYCLE

    #Un nombre de noeuds négatif doit donner une erreur :
    def test_eulerian_cycle_raises_value_error_when_vertices_is_negative(self):
        for nbVertices in range(-3, -1): # V invalides
            for nbEdges in [-3, -1, 0, 3, 5]: # E valides et invalides

                #on s'assure qu'une erreur est lancée
                self.assertRaises(ValueError, generators.eulerianCycle, nbVertices, nbEdges)

    #Un nombre d'arêtes négatif doit donner une erreur  peut importe la valeur de V:
    def test_eulerian_cycle_raises_value_error_when_edge_is_negative(self):
        for V in [10, 0, -10]: # V valides et invalides
            for nbEdges in range(-3, -1): # E invalides

                #on s'assure qu'une erreur est lancée
                self.assertRaises(ValueError, generators.eulerianCycle, V, nbEdges)

    #E > V(V-1)/2 doit donner une erreur
    def test_eulerian_cycle_raises_value_error_when_edges_bigger_than_possible(self):
        for nbVertices in range(1, 10): # V valides
            for nbEdges in range((int)(nbVertices*(nbVertices-1)/2) + 1, (int)(nbVertices*(nbVertices-1)/2) + 3): # E trop gros

                #on s'assure qu'une erreur est lancée
                self.assertRaises(ValueError, generators.eulerianCycle, nbVertices, nbEdges)

    #Test cycle eulerien avec des valeurs valides
    def test_eulerian_cycle(self):
        for nbVertices in range(4, 10):
            for nbEdges in range(4, nbVertices * (nbVertices-1) // 4):

                graph = generators.eulerianCycle(nbVertices, nbEdges)
                self.assertEqual(graph.V(), nbVertices)
                self.assertEqual(graph.E(), nbEdges)

                # on compte combien d'arretes chaque noeud possede
                nbEdgesPerVertice = [0] * nbVertices
                
                for edge in graph.edges():
                    #pour les noeuds qui pointent vers eux memes
                    if (len(edge)==1):
                        nbEdgesPerVertice[list(edge)[0]] += 2
                    else:
                        for v in edge:
                            nbEdgesPerVertice[v] += 1

                #un graphe est un cycle eulerien si et seulement si
                #chaque noeud possede un nombre pair d'arretes
                #(Theoreme d'Euler sur les cycles euleriens)
                for i in nbEdgesPerVertice:
                    self.assertTrue(i%2==0)

#REGULAR

    #Un nombre de noeuds négatif doit donner une erreur :
    def test_regular_raises_value_error_when_vertices_is_negative(self):
        for nbVertices in range(-3, -1): # V invalides
            for nbEdges in [-3, -1, 0, 3, 5]: # E valides et invalides

                #on s'assure qu'une erreur est lancée
                self.assertRaises(ValueError, generators.regular, nbVertices, nbEdges)

    #Un nombre d'arêtes négatif doit donner une erreur  peut importe la valeur de V:
    def test_regular_raises_value_error_when_edge_is_negative(self):
        for V in [10, 0, -10]: # V valides et invalides
            for nbEdges in range(-3, -1): # E invalides

                #on s'assure qu'une erreur est lancée
                self.assertRaises(ValueError, generators.regular, V, nbEdges)

    #E > V(V-1)/2 doit donner une erreur
    def test_regular_raises_value_error_when_edges_bigger_than_possible(self):
        for nbVertices in range(1, 10): # V valides
            for nbEdges in range(nbVertices, nbVertices+3): # E trop gros

                #on s'assure qu'une erreur est lancée
                self.assertRaises(ValueError, generators.regular, nbVertices, nbEdges)

    #Un graphe regulier ne peut exister que si le produit de V et k donne un nombre pair
    def test_regular_when_product_of_V_and_k_is_not_even_should_raise_valueError(self):
        for nbVertices in range(3, 6):
            for nbEdges in range(0, nbVertices):
                if((nbVertices*nbEdges)%2==1):
                    self.assertRaises(ValueError, generators.regular, nbVertices, nbEdges)
                else:
                    generators.regular(nbVertices, nbEdges) # ne doit pas lancer d'erreur

    #Test regular avec des parametres valides
    def test_regular(self):
        for nbVertices in range(3, 6):
            for nbEdges in range(0, nbVertices):
                if((nbVertices*nbEdges)%2==0):
                    graph = generators.regular(nbVertices, nbEdges)
                    self.assertEqual(graph.V(), nbVertices) # test V
                    self.assertEqual(graph.E(), nbEdges * nbVertices // 2) # test E

                    #on compte le nombre d'arretes connectes a chaque noeud
                    nbEdgesPerVertice = [0] * nbVertices

                    for edge in graph.edges():
                        
                        if (len(edge)==1):
                            #pour les noeuds qui pointent vers eux memes
                            nbEdgesPerVertice[list(edge)[0]] += 2
                        else:
                            for v in edge:
                                nbEdgesPerVertice[v] += 1

                    #le graphe est regulier si chaque noeud possede
                    #le meme nombre d'arrete et, dans notre cas, ce
                    #nombre correspond a la valeur desiree
                    for i in nbEdgesPerVertice:
                        self.assertEqual(i, nbEdges)

if __name__ == '__main__':
    unittest.main()