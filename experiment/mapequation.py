# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:26:01 2022

@author: veerl
"""

import networkx as nx
import math
import numpy as np
from sklearn.preprocessing import normalize

# TODO: vector q genereren

def q(graph, communities): 
    'vector of probabilities to go out of a certain community'
    # lengte is aantal communities
    return

    

def p(graph): 
    'Vector p of probabilities to be in a certain node'

    'Get adjacency matrix and normalize, such that columns sum to 1'
    A = nx.to_numpy_matrix(graph)
    A = normalize(A, axis=0, norm='l1') 
    
    'Initialize p, equal probability to start in every node'
    n = graph.number_of_nodes()
    p = np.empty
    p = np.full((n,1), 1/n)
    
    'Performs a max of 100 iterations and unless convergence is met earlier (within an error tolerance)'
    for i in range(100): 
        previous = p
        p=np.matmul(A,p)
        if np.allclose(previous,p, rtol = 1.e-5): #moet deze error tolerance kleiner?
            return p.flatten().tolist()
    
    return p.flatten().tolist()


def p_arrow(communities, p, i): # p_arrow as in paper, without the q term
    result = 0
    for node in communities[i]:
        result += p[node]
    return result

def HQ(communities, q):
    
    def fraction(q, i):
        teller = q[i]
        noemer = sum(q)
        return teller / noemer
    
    result = 0
    for i in len(communities):
        a = fraction(q, i)
        result += a*math.log(a, 2)
    
    return -1*result

def HPi(communities, q, p, i):
    
    p_sum = 0
    for b in communities[i]:
        p_sum += p[b]

    fraction1 = q[i]/(q[i]+p_sum)
    
    result = -1*fraction1*math.log(fraction1,2)
    
    for node in communities[i]:
        a = p[node]/(q[i]+p_sum)
        result -= a*math.log(a,2)
        
    return result


# graph = nx.gnp_random_graph(100, 0.3)
#p = p(graph) # p wil je maar een keer berekenen, die is voor elke keuze van communities hetzelfde, en kost veel tijd

def map_equation(graph, communities, p):
    q = q(graph, communities)
    HQ = HQ(communities, q, p)
    result = sum(q)*HQ
    for i in range(len(communities)):
        p_arrow = p_arrow(communities, p, i)
        HPi = HPi(communities, q, p, i)
        result += (p_arrow*HPi)
    return result
        
