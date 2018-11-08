import matplotlib.pyplot as plt
import networkx as nx
import random

def hierarchy_pos(G, root, decal = 0, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
	"""
		\brief : Crée un dictionnaire servant à l'affichage de l'arbre, chaque noeud a une position x,y
		\param : Le graphe en entier, un noeud
		\return : Un dictionnaire
		\complex : quid complexité .remove() ?
	"""
	#ajuste le décalage
	dec = 0.35 * decal
	
	if pos == None:
		pos = {root:(xcenter,dec+vert_loc)}
	else:
		pos[root] = (xcenter, dec+vert_loc)
	neighbors = list(G.neighbors(root)) 
	if parent != None:   #this should be removed for directed graphs.
		neighbors.remove(parent)  #if directed, then parent not in neighbors.
	if len(neighbors)!=0:
		dx = width/len(neighbors) 
		nextx = xcenter - width/2 - dx/2
		for neighbor in neighbors:
			nextx += dx
			pos = hierarchy_pos(G,neighbor, decal, width = dx, vert_gap = vert_gap, vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, parent = root)                       
	return pos

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
	"""
		\brief:
		\param:
		\return:
		\complex: étant donné qu'on parcourt une seule fois la liste et qu'on place chaque sommet au bon endroit... O(nombre de sommets?)
	"""
	res = [[] for i in range(n_hyper_aretes)]
	for i in range(len(hyper_graph)):
		if len(hyper_graph[i]) != 0: # pas un sommet isolé
			for j in hyper_graph[i]:
				res[j-1].append(i+1)
	return res

def draw_hyper_arete(i,sommets):
	"""
		\brief: dessine une hyper arête
		\param: le numéro de l'hyperarete, la liste de sommets qu'elle relie
		\return: None
	"""
	graph = gen_graph(i,sommets)
	pos = hierarchy_pos(graph,-1,i)
	nx.draw(graph, pos,with_labels=False)
	node_labels = nx.get_node_attributes(graph,'name')
	nx.draw_networkx_labels(graph, pos, labels = node_labels) #affiche les poids a la place des noms
	
def gen_graph(i,sommets):
	"""
		\brief: crée un arbre à partir d'une liste de sommet
		\param: le numéro de l'hyperarete, la liste de sommets qu'elle relie
		\return: un arbre
	"""
	G=nx.Graph()
	G.add_node(-1, name = 'E'+str(i) ) #racine
	for j in range(len(sommets)):
		G.add_node(j,name = 'v'+str(sommets[j]))
		G.add_edge(-1,j)
	return G
	
def launch():
	hyper_graph, n_sommets, n_hyper_aretes = gen_hyper_graph()
	reversed = reverse(hyper_graph,n_hyper_aretes)
	
	for i in range(len(reversed)):
		draw_hyper_arete(i,reversed[i])	
	plt.show()