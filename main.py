#parcourt en post ordre de l'arbre. Si une feuille est négative, on l'élimine, sinon on monte au père. S'il lui + ses enfants sont nég on élimine, sinon on monte.
#On pourrait faire des sauvegardes temporaires des scores des fils quand on monte dans l'arbre pour avoir moins de complexité ?

import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import networkx as nx
import random

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
	n_sommets = random.randint(10,15) #génère entre 10 et 15 sommets
	for i in range(n_sommets):
		pass


G=nx.Graph()
G.add_node(1, weight=-7)
G.add_node(2, weight=4)
G.add_node(3, weight=3)
G.add_node(4, weight=-1)
G.add_node(5, weight=2)
G.add_node(6, weight=4)
G.add_node(7, weight=0)
G.add_node(8, weight=9)
G.add_node(9, weight=-3)
G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(2,4)
G.add_edge(2,5)
G.add_edge(2,6)
G.add_edge(3,7)
G.add_edge(3,8)
G.add_edge(4,9)


pos = hierarchy_pos(G,1)
print(pos)
nx.draw(G, pos=pos, with_labels=False)
node_labels = nx.get_node_attributes(G,'weight')
nx.draw_networkx_labels(G, pos, labels = node_labels)
plt.show()