import matplotlib.pyplot as plt
import networkx as nx
import random

def gen_hyper_graph():
	"""
		\brief : génère un hyper-graphe aléatoire
		\param : /
		\return : dictionnaire de l'hyper-graphe, nombre de sommets, nombre d'arêtes
		\complex : O(nombre de sommets * nombre d'hyper-arêtes)
	"""
	n_sommets = random.randint(5,15)
	n_hyper_aretes = random.randint(3,5)
	hyper_graph = [[] for i in range(n_sommets)]

	for i in range(n_sommets):
		aretes = []
		for j in range(n_hyper_aretes):
			if random.randint(0,1):
				aretes.append(j+1)
		hyper_graph[i] = aretes
		
	return hyper_graph, n_sommets, n_hyper_aretes

def reverse(hyper_graph,n_hyper_aretes):
	res = [[] for i in range(n_hyper_aretes)]
	for i in range(len(hyper_graph)):
		if len(hyper_graph[i]) != 0: # pas un sommet isolé
			for j in hyper_graph[i]:
				res[j-1].append(i+1)
	return res
	
def launch():
	hyper_graph, n_sommets, n_hyper_aretes = gen_hyper_graph()
	print(hyper_graph)
	print(reverse(hyper_graph,n_hyper_aretes))
	"""G, pos = incidence_graph(hyper_graph, n_sommets, n_hyper_aretes)
	nx.draw(G, pos=pos, with_labels=False)
	node_labels = nx.get_node_attributes(G,'number')
	nx.draw_networkx_labels(G, pos, labels = node_labels) #affiche les poids a la place des noms
	"""

	plt.show()