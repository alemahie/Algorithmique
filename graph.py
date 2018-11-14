"""
graph.py

Lemahieu Antoine - 457582
Philips Tristan - 425461
"""

import matplotlib.pyplot as plt
import networkx as nx
import random


	
def hierarchy_pos(G, root, decal = 0, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
	"""
		\brief : Crée un dictionnaire servant à l'affichage de l'arbre, chaque noeud a une position x,y
		\param : Le graphe en entier, un noeud
		\return : Un dictionnaire
		\complex : O(n*profondeur de l'arbre) | n = nombre de sommets.
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
	if len(neighbors)!=0:						#O(n)
		dx = width/len(neighbors) 
		nextx = xcenter - width/2 - dx/2
		for neighbor in neighbors:				  #O(n)
			nextx += dx
			pos = hierarchy_pos(G,neighbor, decal, width = dx, vert_gap = vert_gap, vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, parent = root)                       
	return pos
	
	
	
def gen_graph(i,sommets):
	"""
		\brief : Crée un arbre à partir d'une liste de sommet.
		\param : i, le numéro de l'hyper-arête; somemts, la liste des sommets qu'elle relie.
		\return : Un arbre.
		\complex : O(n²) | n = nombre de sommets.
	"""
	G=nx.Graph()
	G.add_node(-1, name = 'E'+str(i) ) #racine
	for j in range(len(sommets)):					#O(n²)
		G.add_node(j,name = 'v'+str(sommets[j]))	  #O(n)
		G.add_edge(-1,j)							  #O(n)
	return G
	
	
	
def draw_hyper_arete(i,sommets):
	"""
		\brief: Dessine une hyper-arête
		\param: i, le numéro de l'hyper-arête; sommets, la liste des sommets qu'elle relie
		\return: None
		\complex : O(n²) | n = nombre de sommets.
	"""
	graph = gen_graph(i,sommets)			#O(n²)
	pos = hierarchy_pos(graph,-1,i)			#O(n*prodondeur de l'arbre)
	nx.draw(graph, pos,with_labels=False)
	node_labels = nx.get_node_attributes(graph,'name')
	nx.draw_networkx_labels(graph, pos, labels = node_labels) #affiche les poids a la place des noms



def reverse(hyper_graph, n_hyper_aretes):
	"""
		\brief : Créé l'hyper-graphe dual d'un hyper-graphe.
		\param : hyper_graph, une liste de l'hypergraphe; n_hyper_aretes, le nombre d'hyper-arêtes de l'hyper-graphe
		\return : Une liste contenant l'hyper-graphe dual.
		\complex : O(n * nombre d'hyper-arêtes) | n = nombre de sommets.
	"""
	res = [[] for i in range(n_hyper_aretes)]
	for i in range(len(hyper_graph)):		#O(n*nombre d'hyper-arêtes)
		if len(hyper_graph[i]) != 0: # pas un sommet isolé
			for j in hyper_graph[i]:		  #O(nombre d'hyper-arêtes)
				res[j-1].append(i+1)
	return res
	
	
	
def primal_graph(reversed_G):
	"""
		\brief : Crée un graphe primal.
		\param : reversed_G, la liste représentant l'hyper-graphe dual.
		\return : Une liste de paires de noeuds (arêtes) représentant le graphe primal.
		\complex : O(n²*nombre d'hyper-arêtes).
	"""
	res = []
	for i in reversed_G:					#O(n²*nombre d'hyper-arêtes)
		if len(i) > 1:				#Si une hyper-arête contient zéro ou un sommet, il n'a pas de voisins.
			for j in range(len(i)-1):		  #O(n²)
				for k in range(j+1, len(i)):
					x = (i[j],i[k])
					if x not in res:		    #O(n)	#Si l'arête est déjà dans le graphe, ne la met qu'une fois.
						res.append(x)
	return res
	
	
	
def breadth_first_search(n, primal):
	"""
		\brief : Effectue un parcours en largeur lexicographique (Lexicographic breadth-first search / LexBFS).
		\param : n, le nombre de sommets de l'hypergraphe; primal, une liste du graphe primal.
		\return : Une liste contenant les sommets triés par LexBFS.
		\complex : O(n³ * nombre de voisins du sommet) | n = nombre de sommets.
	"""
	L = [[i for i in range(n)]]				#Initialize sequence L
	res = []										#Initialize output
	while len(L) != 0:								#While L not empty						#O(n³*voisins)
		v = L[0][0]									#Find and remove v
		del L[0][0]
		if len(L[0]) == 0:							#Delete empty set
			del L[0]
		res.append(v)								#Add v to res
		voisins_de_v = voisins(primal, v+1)
		replaced = [False for i in range(len(L))]
		for i in voisins_de_v:																  #O(n²*voisins)
			found = False	
			for j in range(len(L)):															    #O(n²)
				if not found and i-1 in L[j]:		#For each edge v_w still in a set		      #O(n)
					found = True
					if not replaced[j]:				#If the set contain w and not replaced, new set
						L.insert(j, [])
						replaced[j] = True
						replaced.insert(j, False)
						L[j].append(i-1)			#Move w
						L[j+1].remove(i-1)
						if len(L[j+1]) == 0:		#If set is empty, delete it
							del L[j+1]
							del replaced[j+1]
					else:							#Move w
						L[j-1].append(i-1)
						L[j].remove(i-1)
						if len(L[j]) == 0:
							del L[j]
							del replaced[j]
	return res
	
	
	
def voisins(primal, x):
	"""
		\brief : Recherche les voisins d'un sommet.
		\param : primal, une liste du graphe primal; x, le sommet dont on cherche les voisins.
		\return : res, une liste contenant tous les voisins du sommet x.
		\complex : O(n²).
	"""
	res = []
	for i in range(len(primal)):			#O(n²)
		if x == primal[i][0]:
			if primal[i][1] not in res:		  #O(n)
				res.append(primal[i][1])
		elif x == primal[i][1]:
			if primal[i][0] not in res:
				res.append(primal[i][0])
	return res
	
	
	
def cordal(primal, bfs):
	"""
		\brief : Vérifie si le graphe est cordal.
		\param : primal, une liste du graphe primal; bfs, une liste résultante du LexBFS.
		\return : True si le graphe est cordal, False sinon.
		\complex : O(n³) | n = nombre de sommets.
	"""
	for i in range(len(bfs)):									  #O(n³)
		voisins_de_v = voisins(primal, bfs[i]+1)
		j = i+1
		found = False
		while j != 1 and not found:									#O(n²)
			j -= 1
			if bfs[j]+1 in voisins_de_v:							   #O(n)
				w = bfs[j]+1			#Voisin de v le plus proche de celui-ci
				found = True
		if found:													#O(n²)							
			voisins_de_w = voisins(primal, w)						  #O(n²)
			for k in range(i, -1, -1):								  #O(n²)
				v_ok, w_ok = False, False
				if bfs[k]+1 in voisins_de_v and bfs[k]+1 != w:		    #O(n)
					v_ok = True
				if k <= j and bfs[k]+1 in voisins_de_w:
					w_ok = True
				if v_ok and not w_ok:
					return False		#v trouvé mais pas w, donc v pas un sous-ensemble de w
	return True
	
	
	
def BronKerbosch(R, P, X, primal, reversed_G, ok):
	"""
		\brief : Trouve les cliques maximales du graphe primal et vérifie si ce sont de hyper-arêtes de l'hypergraphe.
		\param : R, une liste vide; P, l'ensemble des sommets; X, une liste vide; primal, une liste du graphe primal; 
				 reversed_G, une liste de l'hypergraphe dual; ok, conserve le résultat final.
		\return : ok, le résultat final.
		\complex : O(n³.log(n)).
	"""
	if ok:
		if len(P) == 0 and len(X) == 0:
			#print("Maximal Clique : ", R)
			if len(R) >= 2 and R not in reversed_G:
				ok = False
		for i in P:									#O(n³)
			if i not in R:			#R u {v}
				R.append(i)
				R.sort()
			voisins_de_v = voisins(primal, i)
			new_P, new_X = [], []				
			for j in P:				#P n N(v)		  #O(n²)
				if j in voisins_de_v:			 	    #O(n)
					new_P.append(j)			
			for j in X:				#X n N(v)
				if j in voisins_de_v:
					new_X.append(j)
			ok = BronKerbosch(R, new_P, new_X, primal, reversed_G, ok)
			R.remove(i)
			P.remove(i)				#P := P \ {v}
			if i not in X:			#X := X ⋃ {v}
				X.append(i)
				X.sort()
			
	return ok
	
	

def test_hypertree(hyper_graph, n_sommets, n_hyper_aretes):
	"""
		\brief : Test si l'hyper-graphe est un hyper-arbre.
		\param : hyper_graph, une liste contenant l'hypergraphe; n_sommets, le nombre de sommets de l'hypergraphe;
				 n_hyper_aretes, nombre d'hyper-arêtes.
		\return : /
		\complex : O(n³*log(n)).
	"""
	reversed_hyper_graph = reverse(hyper_graph, n_hyper_aretes)		#O(nombre de sommets * nombre d'hyper-arêtes)
	primal = primal_graph(reversed_hyper_graph)						#O(nombre d'hyper-arêtes*n²)

	bfs = breadth_first_search(n_sommets, primal)					#O(n³ * nombre de voisins du sommet)
	verify_cordal = cordal(primal, bfs)								#O(n³)

	verify_max_cliques = BronKerbosch([], [i+1 for i in range(n_sommets)], [], primal, reversed_hyper_graph, True)	#O(n³*log(n))

	print("Vérification graphe cordal : ", verify_cordal)
	print("Vérification cliques maximales sont des hyper-arêtes : ", verify_max_cliques)
	
	if verify_cordal and verify_max_cliques:
		print("L'hyper-graphe est un hyper-arbre.")
	else:
		print("L'hyper-graphe n'est pas un hyper-arbre.")
	
	for i in range(len(reversed_hyper_graph)):
		draw_hyper_arete(i,reversed_hyper_graph[i])	
	plt.show()
