# -*- coding: utf-8 -*-
"""
Created on Mon May 23 13:39:44 2022

@author: veerl
"""

import networkx as nx
import networkx.algorithms.community as nx_comm

# https://networkx.org/documentation/stable/reference/generated/networkx.generators.community.LFR_benchmark_graph.html
# exactly one of min_degree or average_degree must be specified.
# Bedenk welke waarden we willen invullen, welke parameters realistisch zijn
def LFR(n, t1, t2, mu, mincomsize, maxcomsize): #t1, t2 >1, 0<=mu<=1
    return nx.LFR_benchmark_graph(n, t1, t2, mu,min_degree=1 ,min_community = mincomsize, max_community = maxcomsize)

# https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.quality.modularity.html
def modularity(G, communities):
    return nx_comm.modularity(G, communities)

# implement map equation
def entropy(Q):
    return 
def p(g):
    return
def map_equation(G, communities): 
    q = #fraction of time that the random walk spends moving between communities 
    P_g = 
    H_Q = 
    H_P_g = 
    som = 0
    for g in communities:
        som = som + p(g)*entropy(P_g)
    return q * entropy(Q) + som
    
# Implement Louvain for modularity, je moet louvain wel zelf implementeren, anders kun je geen andere objective functie hebben
# Je wil modularity niet de functie pakken altijd, soms moet je alleen delta M hebben als je één node of één community verplaatst, dan is heel M uitrekenen veel langzamer dan delta M

def Louvain_modularity(G):
    communities = {str(i): [i] for i in range(G.number_of_nodes())} #dictionary met communities erin
    communities = [[i] for i in range(G.number_of_nodes())]
    M = modularity(G, communities)
    for node in list(G.nodes()):
        for i in [n for n in G.neighbors(node)]:
            com = communities.copy()
            com[i].append(n)
            com.delete(n)
            M1 = modularity(G, com) #dictionary maken met i : M, dan max eruit halen
            
            
            toren["B"].append(toren["A"].pop())
            

        
    return
    
# implement Louvain for map equation
def Louvain_map_eq(G): # minimize map equation instead of maximize modularity
    return

# implement normalized mutual information
def normalized_mutual_inf():
    return

