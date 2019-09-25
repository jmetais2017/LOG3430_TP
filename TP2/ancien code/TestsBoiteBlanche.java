package tests;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.LinkedList;
import java.util.Queue;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import edu.princeton.cs.algs4.Graph;
import edu.princeton.cs.algs4.GraphGenerator;
import edu.princeton.cs.algs4.SET;

class TestsBoiteBlanche {
	
	@BeforeEach
	void setUp() throws IllegalArgumentException {
	}

	@AfterEach
	void tearDown() throws IllegalArgumentException {
	}

	int count(Iterable<Integer> iterable) {
		int count = 0;
		
		for(int v : iterable)
			count++;
		
		return count;
	}
	
	//methode de cas tests pour le cycle eulerien
	@Test
	void testEulerianCycle() {
		
		//On s'attend à une erreur si le nombre de noeuds est 0 ou négatif
		// T1 = <{V:0, K:10}, {erreur}>
		assertThrows(IllegalArgumentException.class, () -> {
			GraphGenerator.eulerianCycle(0,  10);
		});
		// T2 = <{V:-10, K:10}, {erreur}>
		assertThrows(IllegalArgumentException.class, () -> {
			GraphGenerator.eulerianCycle(-10,  10);
		});
		
		//On s'attend à une erreur si le nombre d'arretes est 0 ou negatif
		// T3 = <{V:10, K:0}, {erreur}>
		assertThrows(IllegalArgumentException.class, () -> {
			GraphGenerator.eulerianCycle(10, -10);
		});
		// T4 = <{V:10, K:0}, {erreur}>
		assertThrows(IllegalArgumentException.class, () -> {
			GraphGenerator.eulerianCycle(10, 0);
		});
		
		//On s'attend à une erreur peut importe le mauvais nombre de noeuds ou d'arretes
		// T5 = <{V:0 ou -10, K:0 ou -10}, {erreur}>
		for(int V : new int[] {0, -10})
			for(int E : new int[] {0, -10})
				assertThrows(IllegalArgumentException.class, () -> {
					GraphGenerator.eulerianCycle(V, E);
				});
		
		//ajout du cas 5 noeuds et une arrete par rapport aux tests en boite noire
		final int[] NB_VERTICES = {5, 10, 100, 1000};
		final int[] NB_EDGES = {1, 50, 500, 5000};
		
		//Pour chaque choix de taille arbitraire du graphe
		for(int i=0 ; i< NB_VERTICES.length ; i++)
		{
			//variables de chaque choix arbitraire
			int nbVertices = NB_VERTICES[i];
			int nbEdges = NB_EDGES[i];
			
			Graph g = GraphGenerator.eulerianCycle(nbVertices, nbEdges);
			
			//on s'attend a ce que chaque noeud ait un nombre pair d'arretes (theoreme d'euler)
			// T6 = <{V: valide, K: valide}, {Graphe tel que pour tout V -> adj(V)%2 = 0}>
			for(int v=0; v<nbVertices; v++)
				assertTrue(count(g.adj(v))%2==0);
			
			int sumVerticesEdges = 0;
			
			for(int v=0; v<nbVertices; v++)
				sumVerticesEdges += count(g.adj(v));
			
			//on s'attend a ce que la somme de chaque noueud possedant une arrete
			//correspond au double du nombre d'arretes definis (lemme des poignees de main)
			// T7 = <{V: valide, K: valide}, {Graphe tel que pour tout V -> somme(adj(V)) = 2*K}>
			assertEquals(nbEdges*2, sumVerticesEdges);
		}
	}
	
	//fonction utilisee dans le test de bipartite permettant de dire si le noeud est
	//dans le premier graphe
	boolean isInFirstGraph(int V1, int V2, int vertice) {
		return vertice >= 0 && vertice < V1;
	}
	
	//fonction utilisee dans le test de bipartite permettant de dire si le noeud est
	//dans le second graphe
	boolean isInSecondGraph(int V1, int V2, int vertice) {
		return vertice >= V1 && vertice < (V1 + V2);
	}
	
	//methode de test pour le graphe bipartite
	@Test
	void testBipartite() {
		
		//On s'attend a une erreur si le nombre de noeuds dans le 1er sous-graphe
		//est negatif
		// T1 = <{V1:-10, V2:10, E:10}, {erreur}>
		assertThrows(IllegalArgumentException.class, () -> {
			GraphGenerator.bipartite(-10, 10, 10);
		});
		
		//On s'attend a une erreur si le nombre de noeuds dans le 2e sous-graphe
		//est negatif
		// T2 = <{V1:10, V2:-10, E:10}, {erreur}>
		assertThrows(IllegalArgumentException.class, () -> {
			GraphGenerator.bipartite(10, -10, 10);
		});
		
		//on s'attend a une erreur si le nombre d'arretes requis est negatif
		// T3 = <{V1:10, V2:10, E:-10}, {erreur}>
		assertThrows(IllegalArgumentException.class, () -> {
			GraphGenerator.bipartite(10, 10, -10);
		});
		
		//on s'attend a une erreur si le nombre de noeuds est negatif pour les
		//deux sous-graphes
		// T4 = <{V1:-10, V2:-10, E:10}, {erreur}>
		assertThrows(IllegalArgumentException.class, () -> {
			GraphGenerator.bipartite(-10, -10, 10);
		});
		
		//on s'attends a une erreur si toutes les valeurs mises dans les arguments sont
		//negatifs
		// T5 = <{V1:-10, V2:-10, E:-10}, {erreur}>
		assertThrows(IllegalArgumentException.class, () -> {
			GraphGenerator.bipartite(-10, -10, -10);
		});
		
		//Test de limite lorsque V1 * V2 - 1 = E
		// T6 = <{V1:10, V2:10, E:99}, {Graphe cree sans erreur}>
		try {
			GraphGenerator.bipartite(10, 10, 99);
		} catch(IllegalArgumentException e) {
			fail("should not have thrown an exception");
		}
		
		//Test de limite lorsque V1 * V2 = E
		// T7 = <{V1:10, V2:10, E:100}, {Graphe cree sans erreur}>
		try {
			GraphGenerator.bipartite(10, 10, 100);
		} catch(IllegalArgumentException e) {
			fail("should not have thrown an exception");
		}
		
		//Test de limite lorsque V1 * V2 + 1 = E
		// T8 = <{V1:10, V2:10, E:101}, {erreur}>
		assertThrows(IllegalArgumentException.class, () -> {
			GraphGenerator.bipartite(10, 10, 101);
		});
		
		//ajout du cas 5 noeuds et une arrete par rapport aux tests en boite noire
		final int[] NB_VERTICES = {5, 10, 100, 1000};
		final int[] NB_EDGES = {1, 5, 50, 500};
		
		//Pour chaque choix de taille arbitraire du graphe
		for(int i=0 ; i< NB_VERTICES.length ; i++)
		{
			//variable de chaque choix arbitraire
			int nbFirstVertices = NB_VERTICES[i];
			int nbSecondVertices = NB_VERTICES[i];
			int nbEdges = NB_EDGES[i];
			
			Graph g = GraphGenerator.bipartite(nbFirstVertices, nbSecondVertices, nbEdges);
			
			int nbVertices = nbFirstVertices + nbSecondVertices;
			int sumVerticesEdges = 0;
			
			for(int v=0; v<nbVertices; v++)
				sumVerticesEdges += count(g.adj(v));
			
			//on s'attend a ce que la somme de chaque noueud possedant une arrete
			//correspond au double du nombre d'arretes definis (lemme des poignees de main)
			// T9 = <{V1: valide, V2: valide, E: valide}, {Graphe tel que pour tout V -> somme(adj(V)) = 2*E}>
			assertEquals(nbEdges*2, sumVerticesEdges);
			
			//
			//A partir d'ici, le test va verifier que le graphe possede bel et bien
			//2 sous-graphes bipartites en mettant chaque noeud du graphe dans un
			//ensemble selon dans le sous-graphe dans lequel il y est
			//
			SET<Integer> set1 = new SET<Integer>();
			SET<Integer> set2 = new SET<Integer>();
			
			Queue<Integer> queue = new LinkedList<Integer>();
			
			int chosenVertice = 0;
			
			//On cherche un noeud qui possede des arretes
			while(count(g.adj(chosenVertice)) == 0)
				chosenVertice++;
			
			//on ajoute ce noued dans la queue
			queue.add(chosenVertice);
			
			while(!queue.isEmpty()) {
				int current = queue.poll();
				
				SET<Integer> currentSet = null;
				SET<Integer> otherSet = null;
				
				//Si le noeud appartient dans aucun des 2 sous ensemble, on le met
				//arbitrairement dans le 1er sous-ensemble
				if(!set1.contains(current) && !set2.contains(current)) {
					currentSet = set1;
					otherSet = set2;
					currentSet.add(current);
				}
				else if(set1.contains(current)) {
					currentSet = set1;
					otherSet = set2;
				} else if (set2.contains(current)) {
					currentSet = set2;
					otherSet = set1;
				}
				
				//pour chaque enfant du noeud courant analyse, on s'attend a ce qu'il ne soit
				//pas dans le meme sous-ensemble que son pere
				for(int child : g.adj(current)) {
					// T10 = <{V1: valide, V2: valide, E: valide},
					// {Graphe tel que pour tout V -> tout enfant de V -> sousGraphe(V) != sousGraphe(Enfant)}>
					assertFalse(currentSet.contains(child));
					
					if(!otherSet.contains(child)) {
						otherSet.add(child);
						queue.add(child);
					}
				}
			}	
		}
	}
	
	//Methode de test pour le generateur de graphes regulier
	@Test
	void testRegular() {
		
		//On s'attend a une erreur si le nombre de noeuds definis est negatif
		// T1 = <{V:-10, K:10},{erreur}>
		assertThrows(IllegalArgumentException.class, () -> {
			GraphGenerator.regular(-10,  10);
		});
		
		//On s'attend a une erreur si le nombre d'arretes definis est negatif
		// T2 = <{V:10, K:-10},{erreur}>
		assertThrows(NegativeArraySizeException.class, () -> {
			GraphGenerator.regular(10, -10);
		});
		
		//On s'attend a une erreur si les 2 parametres sont negatifs
		// T3 = <{V:-10, K:-10},{erreur}>
		assertThrows(IllegalArgumentException.class, () -> {
			GraphGenerator.regular(-10, -10);
		});
		
		//On s'attend a une erreur si K et V sont tous les 2 impairs
		// T4 = <{V:impair, K:impair},{erreur}>
		for(int V : new int[]{9,11,13,15})
			for(int K : new int[] {1,3,5,7,9})
			assertThrows(IllegalArgumentException.class, () -> {
				GraphGenerator.regular(V, K);
			});
		
		final int[] NB_VERTICES = {5, 10, 100, 1000};
		final int[] NB_EDGES = {0, 5, 50, 500};
		
		//Pour chaque choix de taille arbitraire du graphe
		for(int i=0 ; i< NB_VERTICES.length ; i++)
		{
			//variables de chaque choix arbitraire
			int nbVertices = NB_VERTICES[i];
			int nbEdges = NB_EDGES[i];
			
			Graph g = GraphGenerator.regular(nbVertices, nbEdges);
			
			//On s'attend a ce que le nombre d'arretes de chaque noeud correspond
			//au nombre d'arretes specifies dans le generateur
			//T5 = <{V, E}, {Graphe tel que pour tout V -> adj(V) = E}>
			for(int v=0; v<nbVertices; v++)
				assertTrue(count(g.adj(v)) == nbEdges);
		}
	}
}
