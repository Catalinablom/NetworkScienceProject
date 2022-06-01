# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:26:01 2022

@author: veerl
"""

import networkx as nx
import math
import numpy as np
import sklearn
from sklearn.preprocessing import normalize

def LFR(n, t1, t2, mu, mincomsize, maxcomsize): #t1, t2 >1, 0<=mu<=1
    return nx.LFR_benchmark_graph(n, t1, t2, mu,min_degree=1 ,min_community = mincomsize, max_community = maxcomsize)

graph = LFR(10, 2.5, 2.5, 0.3,3, 10)
communities = {frozenset(graph.nodes[v]["community"]) for v in graph}



def p_arrow(communities, p, i): # p_arrow as in paper, without the q term
    result = 0
    for node in list(communities)[i]:
        result += p[node]
    return result


def calculate_q(graph, communities, p): 
    'vector of probabilities to go out of a certain community'
    q = []
    # lengte is aantal communities
    def calculate_qi(alpha):
        if len(list(communities)[alpha])==0:
            return 0
        result = 0
        for node in list(communities)[alpha]:
            edges_uit=0
            for neighbour in graph.neighbors(node):
                if neighbour not in list(communities)[alpha]:
                    edges_uit += 1
        result += (p[node]/p_arrow(communities, p, alpha))*(edges_uit / graph.degree(node))
        
        return result
    
    for i in range(len(communities)):
        qi = calculate_qi(i)
        q.append(qi)    
    return q

    

def calculate_p(graph): 
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
        p = np.matmul(A,p)        
        if np.allclose(previous,p, rtol = (1.e-5)/n): #moet deze error tolerance kleiner?
            return p.flatten().tolist()
    
    return p.flatten().tolist()




def calculate_HQ(communities, q):
    
    def fraction(q, i):
        teller = q[i]
        noemer = sum(q)
        if noemer == 0 :
            return 0
        return teller / noemer
    
    result = 0
    for i in range(len(communities)):
        a = fraction(q, i)
        if a == 0:
            result += 0
        else:
            result += a*math.log(a, 2)
    
    return -1*result

def calculate_HPi(communities, q, p, i):
    
    p_sum = 0
    for b in list(communities)[i]:
        p_sum += p[b]
    if (q[i]+p_sum) == 0:
        fraction1 = 0
    else:
        fraction1 = q[i]/(q[i]+p_sum)
    
    if fraction1 == 0:
        result = 0
    else:
        result = -1*fraction1*math.log(fraction1,2)
    
    for node in list(communities)[i]:
        a = p[node]/(q[i]+p_sum)
        if a == 0:
            result -= 0
        else:
            result -= a*math.log(a,2)
        
    return result

p = calculate_p(graph) # p wil je maar een keer berekenen, die is voor elke keuze van communities hetzelfde, en kost veel tijd

def map_equation(graph, communities, p):
    q = calculate_q(graph, communities, p)
    HQ = calculate_HQ(communities, q)
    result = sum(q)*HQ
    for i in range(len(communities)):
        p_a = p_arrow(communities, p, i)
        HPi = calculate_HPi(communities, q, p, i)
        result += (p_a*HPi)
    return result
        
        
print('mapeq:', map_equation(graph, communities, p))
# print*map_equation(graph,communities,p)