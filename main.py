#parcourt en post ordre de l'arbre. Si une feuille est negative, on l'elimine, sinon on monte au pere. S'il lui + ses enfants sont neg on elimine, sinon on monte.
#On pourrait faire des sauvegardes temporaires des scores des fils quand on monte dans l'arbre pour avoir moins de complexite ?

import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import networkx as nx
import random

#########################################################################################################

def hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
	if pos == None:
		#pos = {G.node[root]['weight']:(xcenter,vert_loc)}
		pos = {root:(xcenter,vert_loc)}
	else:
		pos[root] = (xcenter, vert_loc)
	neighbors = list(G.neighbors(root)) 
	if parent != None:   #this should be removed for directed graphs.
		neighbors.remove(parent)  #if directed, then parent not in neighbors.
	if len(neighbors)!=0:
		dx = width/len(neighbors) 
		nextx = xcenter - width/2 - dx/2
		for neighbor in neighbors:
			nextx += dx
			pos = hierarchy_pos(G,neighbor, width = dx, vert_gap = vert_gap, vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, parent = root)                       
	return pos


def gen_sommet():
	"""
		\brief : cree un arbre de 10 a 15 sommets, dont chacun a un poids de -10 à 10
		\param : None
		\return : un arbre
	"""
	G=nx.Graph()
	n_sommets = random.randint(10,15) #genere entre 10 et 15 sommets
	for i in range(n_sommets):
		G.add_node(i+1, weight = random.randint(-5,10)) #Cree un noeud aleatoire
		if i != 0:
			G.add_edge(random.randint(1, i), i+1) #Relie ce nouveau noeud (sauf le premier), aleatoirement parmi les precedents
	return G
	
	

def delete_node(G,N):
	"""
		\brief : supprime un noeud et tous ses voisins sauf son père. Si c'est une feuille, supprme uniquement la feuille
		\param : l'arbre, un noeud
		\return : l'arbre amputé du noeud et de ses éventuels fils
		\complex : 
	"""
	fils = list(G.neighbors(N))[1:]
	for i in fils:
		G = delete_node(G, i)
	G.remove_node(N)
	return G
	
	

def sous_somme(voisins, somme_des_fils, dec):
	somme = 0
	for i in voisins[dec:]:
		somme += somme_des_fils[i]
	return somme
	
	

def max_subtree(i, node_labels, somme_des_fils, G):
	voisins = list(G.neighbors(i))
	if i != 1:
		for j in range(len(voisins)-1):
			G = max_subtree(voisins[j+1], node_labels, somme_des_fils, G)
		if voisins[1:] == [] and node_labels[i] > 0:		#Si feuille > 0, ok
			somme_des_fils[i] = node_labels[i]
		elif voisins[1:] == [] and node_labels[i] <= 0:		#Si feuilles <= 0, bye bye
			somme_des_fils[i] = 0
			G = delete_node(G, i)
		if voisins[1:] != [] and node_labels[i] <= 0:	 	#Si pas feuille < 0, check sous-arbre
			somme = sous_somme(voisins, somme_des_fils, 1)
			somme_des_fils[i] = somme
			if somme + node_labels[i] > 0:					#Si noeud + fils > 0, ok
				somme_des_fils[i] += node_labels[i]
			else:											#Si noeud + fils <= 0, bye bye
				somme_des_fils[i] = 0
				G = delete_node(G, i)
		elif voisins[1:] != [] and node_labels[i] > 0:		#Si pas feuille > 0, ok
			somme = sous_somme(voisins, somme_des_fils, 1)
			somme_des_fils[i] = somme + node_labels[i]
	else:
		for j in voisins:
			G = max_subtree(j, node_labels, somme_des_fils, G)
				
		somme = sous_somme(voisins, somme_des_fils, 0)
		somme_des_fils[i] = somme + node_labels[i]
				
		if somme_des_fils[i] > 0:		
			return G
		else:							#Aucun arbre max > 0
			res = nx.Graph()
			res.add_node(1, weight = 0)
			return res
	return G
	
	

##########################################################################################################

G = gen_sommet()   

pos = hierarchy_pos(G,1)
nx.draw(G, pos=pos, with_labels=False)
node_labels = nx.get_node_attributes(G,'weight')
nx.draw_networkx_labels(G, pos, labels = node_labels) #affiche les poids a la place des noms
plt.show()

G = max_subtree(1, node_labels, {}, G)

pos = hierarchy_pos(G,1)
nx.draw(G, pos=pos, with_labels=False)
node_labels = nx.get_node_attributes(G,'weight')
nx.draw_networkx_labels(G, pos, labels = node_labels) #affiche les poids a la place des noms
plt.show()
