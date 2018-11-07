import matplotlib.pyplot as plt
import networkx as nx
import random

def incidence_graph(hyper_graph, n_sommets, n_hyper_aretes):
	"""
		\brief : graphe d'incidence de l'hyper-graphe
		\param : dictionnaire de l'hyper-graphe, nombre de sommets, nombre d'hyper arêtes
		\return : graphe, position des noeuds
		\complex : O(nombre de sommets + nombre d'hyper arêtes
	"""
	G = nx.Graph()
	pos = {}
	
	for i in range(n_sommets + n_hyper_aretes):
		if i < n_sommets:
			pos[i+1] = (0.0, -0.5*i)
			G.add_node(i+1, number = i+1)
		else:
			pos[i+1] = (0.05, -0.5*(i-n_sommets))
			G.add_node(i+1, number = i-n_sommets+1)

	for i in range(n_sommets):
		for j in hyper_graph[i]:
			G.add_edge(i+1, j+n_sommets+1)

	return G, pos
		
def gen_hyper_graph():
	"""
		\brief : génère un hyper-graphe aléatoire
		\param : /
		\return : dictionnaire de l'hyper-graphe, nombre de sommets, nombre d'arêtes
		\complex : O(nombre de sommets * nombre d'hyper-arêtes)
	"""
	n_sommets = random.randint(5,15)
	n_hyper_aretes = random.randint(3,5)
	hyper_graph = {}

	for i in range(n_sommets):
		aretes = []
		for j in range(n_hyper_aretes):
			if random.randint(0,1):
				aretes.append(j)
		hyper_graph[i] = aretes
		
	return hyper_graph, n_sommets, n_hyper_aretes

def launch():
	hyper_graph, n_sommets, n_hyper_aretes = gen_hyper_graph()
	print(hyper_graph)
	G, pos = incidence_graph(hyper_graph, n_sommets, n_hyper_aretes)
	nx.draw(G, pos=pos, with_labels=False)
	node_labels = nx.get_node_attributes(G,'number')
	nx.draw_networkx_labels(G, pos, labels = node_labels) #affiche les poids a la place des noms

	plt.show()