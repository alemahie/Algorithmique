"""
algo2_2018.py

Lemahieu Antoine - 457582
Philips Tristan - 425461
"""

import tree
import graph
import networkx as nx
import random



def gen_tree():
	"""
		\brief : Créé un arbre aléatoire de 10 à 15 sommets, dont chacun a un poids de -10 à 10.
		\param : None.
		\return : Un arbre aléatoire.
		\complex : O(n²) | n = nombre de sommets
	"""
	G=nx.Graph()
	n_sommets = random.randint(10,15) #genere entre 10 et 15 sommets
	for i in range(n_sommets):						  #O(n²)
		G.add_node(i+1, weight = random.randint(-10,10)) 		#Crée un noeud aleatoire
		if i != 0:
			G.add_edge(random.randint(1, i), i+1) 		#O(n)	#Relie ce nouveau noeud (sauf le premier), aleatoirement parmi les precedents
	return G



def gen_hyper_graph():
	"""
		\brief : Génère un hyper-graphe aléatoire.
		\param : /
		\return : hyper-graph, une liste contenant l'hyper-graphe; n_sommets, le nombre de sommets; n_hyper_aretes, le nombre d'hyper-arêtes.
		\complex : O(nombre de sommets * nombre d'hyper-arêtes).
	"""
	n_sommets = random.randint(5,15)
	n_hyper_aretes = random.randint(3,5)
	hyper_graph = [[] for i in range(n_sommets)]

	for i in range(n_sommets):			  #O(nombre de sommets * nombre d'hyper-arêtes)
		aretes = []
		for j in range(n_hyper_aretes):		#O(nombre d'hyper-arêtes)
			if random.randint(0,1):
				aretes.append(j+1) 
		hyper_graph[i] = aretes
		
	return hyper_graph, n_sommets, n_hyper_aretes



def main():
	G = gen_tree()
	tree.max_subtree(G)
	
	print("\n\n	Hyper-graphe :")
	hyper_graph, n_sommets, n_hyper_aretes = gen_hyper_graph()
	graph.test_hypertree(hyper_graph, n_sommets, n_hyper_aretes)

if __name__ == '__main__':
	main()
