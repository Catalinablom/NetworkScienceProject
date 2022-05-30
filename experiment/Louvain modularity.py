# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:08:47 2022

@author: veerl

"""
import networkx as nx
import networkx.algorithms.community as nx_comm

def modularity(G, communities):
    return nx_comm.modularity(G, communities)

def geefkey(dictionary, value):
    for key, i in dictionary.items():
        if i != []:
            if value in i:
                return key #maak dit nog naar int, nu str
    return False

def Louvain_modularity(G):
    communities = {str(i): [i] for i in range(G.number_of_nodes())} #dictionary met communities erin
    
    for node in list(G.nodes()):
        deltaMmax = 0
        moveto = 0
        M = modularity(G, communities)
        for i in G.neighbors(node):
            com = communities.copy()
            com[geefkey(com, i)].append(com[str(node)].pop())
            deltaM = modularity(G, com) - M #delta M bepalen op andere snellere methode
            if deltaM > deltaMmax:
                deltaMmax = deltaM
                moveto = i
        if deltaMmax > 0:
            communities[str(moveto)].append(communities[str(node)].pop())
        
            
    
                
            

        
    return