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
	
	
	
def gen_graph(i,sommets):
	"""
		\brief : Crée un arbre à partir d'une liste de sommet.
		\param : i, le numéro de l'hyper-arête; somemts, la liste des sommets qu'elle relie.
		\return : Un arbre.
		\complex : 
	"""
	G=nx.Graph()
	G.add_node(-1, name = 'E'+str(i) ) #racine
	for j in range(len(sommets)):
		G.add_node(j,name = 'v'+str(sommets[j]))
		G.add_edge(-1,j)
	return G
	
	
	
def draw_hyper_arete(i,sommets):
	"""
		\brief: Dessine une hyper-arête
		\param: i, le numéro de l'hyper-arête; sommets, la liste des sommets qu'elle relie
		\return: None
		\complex : 
	"""
	graph = gen_graph(i,sommets)
	pos = hierarchy_pos(graph,-1,i)
	nx.draw(graph, pos,with_labels=False)
	node_labels = nx.get_node_attributes(graph,'name')
	nx.draw_networkx_labels(graph, pos, labels = node_labels) #affiche les poids a la place des noms





def reverse(hyper_graph, n_hyper_aretes):
	"""
		\brief : Créé l'hyper-graphe dual d'un hyper-graphe.
		\param : hyper_graph, une liste de l'hypergraphe; n_hyper_aretes, le nombre d'hyper-arêtes de l'hyper-graphe
		\return : Une liste contenant l'hyper-graphe dual.
		\complex : 
	"""
	res = [[] for i in range(n_hyper_aretes)]
	for i in range(len(hyper_graph)):
		if len(hyper_graph[i]) != 0: # pas un sommet isolé
			for j in hyper_graph[i]:
				res[j-1].append(i+1)
	return res
	
	
	
def primal_graph(reversed_G):
	"""
		\brief : Crée un graphe primal.
		\param : reversed_G, la liste représentant l'hyper-graphe dual.
		\return : Une liste de paires de noeuds (arêtes) représentant le graphe primal.
		\complex : O(nombre d'hyper-arêtes * nombres de noeuds voisins à chaques noeuds)
	"""
	res = []
	for i in reversed_G:
		if len(i) > 1:
			for j in range(len(i)-1):
				for k in range(j+1, len(i)):
					x = (i[j],i[k])
					if x not in res:
						res.append(x)
	return res
	
	
	
def breadth_first_search(n, primal):
	"""
		\brief : Effectue un parcours en largeur lexicographique (Lexicographic breadth-first search / LexBFS).
		\param : n, le nombre de sommets de l'hypergraphe; primal, une liste du graphe primal.
		\return : Une liste contenant les sommets triés par LexBFS.
		\complex : 
	"""
	L = [[i for i in range(n)]]				#Initialize sequence L
	res = []										#Initialize output
	while len(L) != 0:								#While L not empty
		v = L[0][0]									#Find and remove v
		del L[0][0]
		if len(L[0]) == 0:							#Delete empty set
			del L[0]
		res.append(v)								#Add v to res
		voisins_de_v = voisins(primal, v+1)
		replaced = [False for i in range(len(L))]
		for i in voisins_de_v:		
			found = False	
			for j in range(len(L)):
				if not found and i-1 in L[j]:		#For each edge v_w still in a set
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
		\complex : O(1) / O(nombre d'éléments dans primal)
	"""
	res = []
	for i in range(len(primal)):
		if x == primal[i][0]:
			if primal[i][1] not in res:
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
		\complex : 
	"""
	for i in range(len(bfs)):
		voisins_de_v = voisins(primal, bfs[i]+1)
		j = i+1
		found = False
		while j != 1 and not found:
			j -= 1
			if bfs[j]+1 in voisins_de_v:	
				w = bfs[j]+1			#Voisin de v le plus proche de celui-ci
				found = True
		if found:
			voisins_de_w = voisins(primal, w)
			new_voisins_v, new_voisins_w = [], []
			for k in range(i, -1, -1):
				if bfs[k]+1 in voisins_de_v and bfs[k]+1 != w:
					new_voisins_v.append(bfs[k]+1)
				if k <= j and bfs[k]+1 in voisins_de_w:
					new_voisins_w.append(bfs[k]+1)
			for k in new_voisins_v:
				if k not in new_voisins_w:
					return False
	return True
	
	
	
def BronKerboschl(R, P, X, primal, reversed_G, ok):
	"""
		\brief : Trouve les cliques maximales du graphe primal et vérifie si ce sont de hyper-arêtes de l'hypergraphe.
		\param : R, une liste vide; P, l'ensemble des sommets; X, une liste vide; primal, une liste du graphe primal; 
				 reversed_G, une liste de l'hypergraphe dual; ok, conserve le résultat final.
		\return : ok, le résultat final.
		\complex : 
	"""
	if ok:
		if len(P) == 0 and len(X) == 0:
			print("Maximal Clique : ", R)
			if len(R) >= 2 and R not in reversed_G:
				ok = False
		for i in P:
			if i not in R:			#R u {v}
				R.append(i)
				R.sort()
			voisins_de_v = voisins(primal, i)
			new_P = []				#P n N(v)
			for j in P:
				if j in voisins_de_v:
					new_P.append(j)
			new_X = []				#X n N(v)
			for j in X:
				if j in voisins_de_v:
					new_X.append(j)
			ok = BronKerboschl(R, new_P, new_X, primal, reversed_G, ok)
			R.remove(i)
			P.remove(i)				#P := P \ {v}
			if i not in X:			#X := X ⋃ {v}
				X.append(i)
				X.sort()
			
	return ok
	
	

def test_hypertree(hyper_graph):
	"""
	Test hypertree
	"""
	print("coucou")
	
	
def launch():
	hyper_graph, n_sommets, n_hyper_aretes = gen_hyper_graph()
	
	"""
			#Hyper_graph test, est un hyper_tree.
	hyper_graph = [[1], [1,2], [1,2,3], [4], [3], [3], []]
	n_sommets = 7
	n_hyper_aretes = 4
	
			#Hyper_graph test, n'est pas un hyper_tree.
	hyper_graph = [[1,2],[1],[1,3],[4],[2,3],[3],[]]
	n_sommets = 7
	n_hyper_aretes = 4
	"""
	
	reversed_hyper_graph = reverse(hyper_graph, n_hyper_aretes)
	primal = primal_graph(reversed_hyper_graph)
	
	print("Nombre sommets : ", n_sommets)
	print("Nombre d'hyper arêtes : ", n_hyper_aretes)
	print("Par sommets : ", hyper_graph)
	print("Par hyper aretes : ", reversed_hyper_graph)
	print("Primal ; ", primal)
	
	"""
	G, pos = incidence_graph(hyper_graph, n_sommets, n_hyper_aretes)
	nx.draw(G, pos=pos, with_labels=False)
	node_labels = nx.get_node_attributes(G,'number')
	nx.draw_networkx_labels(G, pos, labels = node_labels) #affiche les poids a la place des noms
	"""
	
	bfs = breadth_first_search(n_sommets, primal)
	verify_cordal = cordal(primal, bfs)

	verify_max_cliques = BronKerboschl([], [i+1 for i in range(n_sommets)], [], primal, reversed_hyper_graph, True)

	print("\n\n\n\nVerify cordal : ", verify_cordal)
	print("Verify max cliques : ", verify_max_cliques)
	
	if verify_cordal and verify_max_cliques:
		print("L'hyper-graphe est un hyper-arbre.")
	else:
		print("L'hyper-graphe n'est pas un hyper-arbre.")
	
	
	for i in range(len(reversed_hyper_graph)):
		draw_hyper_arete(i,reversed_hyper_graph[i])	
	plt.show()
