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
	"""
		\brief : 
		\param : 
		\return : 
		\complex : 
	"""
	res = [[] for i in range(n_hyper_aretes)]
	for i in range(len(hyper_graph)):
		if len(hyper_graph[i]) != 0: # pas un sommet isolé
			for j in hyper_graph[i]:
				res[j-1].append(i+1)
	return res
	
	
	
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
	
	
	

def primal_graph(reversed_G):
	"""
		\brief : 
		\param : 
		\return : 
		\complex : 
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
	
	
	
def breadth_first_search(G, primal):
	"""
		\brief : 
		\param : 
		\return : 
		\complex : 
	"""
	L = [[i for i in range(len(G))]]				#Initialize sequence L
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
						L[j].append(i-1)			#Move <
						L[j+1].remove(i-1)
						if len(L[j+1]) == 0:
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
		\brief : 
		\param : 
		\return : 
		\complex : 
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
		\brief : 
		\param : 
		\return : 
		\complex : 
	"""
	for i in range(len(bfs)):
		print("i : ", i)
		voisins_de_v = voisins(primal, bfs[i]+1)
					# i = indice, bfs[i]+1 = valeur
					
		j = i+1
		found = False
		while j != 1 and not found:
			j -= 1
			if bfs[j]+1 in voisins_de_v:	
				w = bfs[j]+1	#Voisin de i le plus proche de celui-ci
				found = True

		print("j : ", j)

		if found:
			
			#v, w et voisins => -1 dans lex BFS
			#i et j  position dans lexBFS
			
			
			voisins_de_w = voisins(primal, w)
			print("Lex BFS : ", bfs)
			print("v : ", bfs[i]+1)
			print("w : ", w)
			print("voisins de v : ", voisins_de_v)
			print("voisins de w : ", voisins_de_w)
		
			new_voisins_v = []
			new_voisins_w = []
			for k in range(i, -1, -1):
				if bfs[k]+1 in voisins_de_v and bfs[k]+1 != w:
					new_voisins_v.append(bfs[k]+1)
				if k <= j and bfs[k]+1 in voisins_de_w:
					new_voisins_w.append(bfs[k]+1)
					
			print("Voisins précedants de v : ", new_voisins_v)
			print("Voisins précedants de w : ", new_voisins_w)
			
			for k in new_voisins_v:
				if k not in new_voisins_w:
					return False
	return True
	
	
	
def BronKerboschl(R, P, X, primal, reversed_G, ok):
	"""
		\brief : 
		\param : 
		\return : 
		\complex : 
	"""
	if ok:
		if len(P) == 0 and len(X) == 0:
			print("Maximal Clique : ", R)
			if len(R) >= 2 and R not in reversed_G:
				ok = False
				
		for i in P:
				#R u {v}
			if i not in R:		
				R.append(i)
				R.sort()
				
			voisins_de_v = voisins(primal, i)
				#P n N(v)
			new_P = []
			for j in P:
				if j in voisins_de_v:
					new_P.append(j)
				#X n N(v)
			new_X = []
			for j in X:
				if j in voisins_de_v:
					new_X.append(j)
			ok = BronKerboschl(R, new_P, new_X, primal, reversed_G, ok)
				
			R.remove(i)
				#P := P \ {v}
			P.remove(i)
				#X := X ⋃ {v}
			if i not in X:
				X.append(i)
				X.sort()
			
	return ok
	
	
def launch():
	hyper_graph, n_sommets, n_hyper_aretes = gen_hyper_graph()
	
	#hyper_graph = [[1], [1,2], [1,2,3], [4], [3], [3], []]
	n_sommets = 7
	n_hyper_aretes = 4
			#Hyper tree
	hyper_graph = [[1,2],[1],[1,3],[4],[2,3],[3],[]]

	
	reversed_hyper_graph = reverse(hyper_graph,n_hyper_aretes)
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

	bfs = breadth_first_search(hyper_graph, primal)
	verify_cordal = cordal(primal, bfs)

	
	print(reversed_hyper_graph)
	verify_max_cliques = BronKerboschl([], [i+1 for i in range(n_sommets)], [], primal, reversed_hyper_graph, True)

	print("\n\n\n\nVerify cordal : ", verify_cordal)
	print("Verify max cliques : ", verify_max_cliques)
	
	if verify_cordal and verify_max_cliques:
		print("				C bon c ok mdr")
	else:
		print("				C de la merde ton truk")
	
	plt.show()
