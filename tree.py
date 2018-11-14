import matplotlib.pyplot as plt
import networkx as nx
import random

def hierarchy_pos(G, root, second = False, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
	"""
		\brief : Crée un dictionnaire servant à l'affichage de l'arbre, chaque noeud a une position x,y.
		\param : G, le graphe entier; root, un noeud pris comme racine.
		\return : Un dictionnaire de postions des noeuds.
		\complex : O(n * profondeur de l'arbre) | n = nombre de sommets.
	"""
		#Ajuste le décalage si on est dans le second arbre
	if second: dec = 1.2
	else: dec = 0
		
	if pos == None:
		pos = {root:(dec+xcenter,vert_loc)}
	else:
		pos[root] = (dec+xcenter, vert_loc)
	neighbors = list(G.neighbors(root)) 
	if parent != None:   #this should be removed for directed graphs.
		neighbors.remove(parent)  #if directed, then parent not in neighbors.
	if len(neighbors)!=0:
		dx = width/len(neighbors) 
		nextx = xcenter - width/2 - dx/2
		for neighbor in neighbors:
			nextx += dx
			pos = hierarchy_pos(G,neighbor, second, width = dx, vert_gap = vert_gap, vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, parent = root)                       
	return pos
	
	

def delete_node(G,N):
	"""
		\brief : Supprime un noeud et tous ses voisins sauf son père. Si c'est une feuille, supprime uniquement la feuille.
		\param : G, l'arbre; N, un noeud depuis lequel il faut supprimer.
		\return : L'arbre amputé du noeud et de ses éventuels fils.
		\complex : O(n * profondeur des fils)
	"""
	fils = list(G.neighbors(N))[1:]
	for i in fils:					#O(n)
		G = delete_node(G, i)
	G.remove_node(N)				#O(n)
	return G
	
	

def sous_somme(voisins, somme_des_fils, dec):
	"""
		\brief : Somme les valeurs des fils afin d'avoir la valeur totale du sous-arbre.
		\param : voisins, une liste des voisins du noeud; somme_des_fils, un dictionnaire contenant la somme des fils de tous les noeuds;
				 dec, un décalage (0 si racine, 1 sinon)
		\return : La somme calculée
		\complex : O(nombre de voisins).
	"""
	somme = 0
	for i in voisins[dec:]:
		somme += somme_des_fils[i]
	return somme
	
	

def reduc_tree(i, node_labels, somme_des_fils, G):
	"""
		\brief : Réduit l'arbre donné afin de calculer le sous-arbre dont la somme des noeuds est maximale.
		\param : i, le numéro du noeud d'où l'on part; node_labels, un dictionnaire contenant la valeur de tous les noeuds;
				 somme_des_fils, un dictionnaire contenant la somme des fils de tous les noeuds; G, l'arbre en question.
		\return : Un arbre sous-tendant maximum.
		\complex : O(n * profondeur de l'arbre).
	"""
	voisins = list(G.neighbors(i))
	if i != 1:
		for j in range(len(voisins)-1):					#O(n*profondeur de l'arbre)
			G = reduc_tree(voisins[j+1], node_labels, somme_des_fils, G)	#Récursivité jusqu'aux feuilles.
		if voisins[1:] == [] and node_labels[i] > 0:		#Si feuille > 0, ok
			somme_des_fils[i] = node_labels[i]
		elif voisins[1:] == [] and node_labels[i] <= 0:		#Si feuilles <= 0, bye bye
			somme_des_fils[i] = 0
			G = delete_node(G, i)						  #O(n*profondeur des fils)
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
			G = reduc_tree(j, node_labels, somme_des_fils, G)
				
		somme = sous_somme(voisins, somme_des_fils, 0)
		somme_des_fils[i] = somme + node_labels[i]
				
		if somme_des_fils[i] > 0:		
			return G
		else:							#Aucun arbre max > 0
			res = nx.Graph()
			res.add_node(1, weight = 0)
			return res
	return G
	
	
	
def max_subtree(G):
	"""
		\brief : Génère un arbre aléatoire et calcule son arbre sous-tendant maximum.
		\param : G, une liste représentant un arbre.
		\return : /
		\complex : O(n * profondeur de l'arbre).
	"""
		#Arbre initial
	pos = hierarchy_pos(G,1)
	nx.draw(G, pos=pos, with_labels=False)
	node_labels = nx.get_node_attributes(G,'weight')
	nx.draw_networkx_labels(G, pos, labels = node_labels) #Affiche les poids à la place des noms.

		#Arbre recoupé
	G = reduc_tree(1, node_labels, {}, G) 	#Réduction de l'arbre.
	pos = hierarchy_pos(G,1,True)
	nx.draw(G, pos=pos, with_labels=False)
	node_labels = nx.get_node_attributes(G,'weight')
	nx.draw_networkx_labels(G, pos, labels = node_labels)
	plt.show() 		#Affichage
