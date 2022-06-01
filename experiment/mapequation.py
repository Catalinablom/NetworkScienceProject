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



def p_arrow(communities, p, i): # p_arrow as in paper, without the q term
    result = 0
    for node in communities[i]:
        result += p[node]
    return result


def calculate_q(graph, communities, p): 
    'vector of probabilities to go out of a certain community'
    q = []
    # lengte is aantal communities
    def calculate_qi(alpha):
        result = 0
        for node in communities[alpha]:
            edges_uit=0
            for neighbour in graph.neighbors(node):
                if neighbour not in communities[alpha]:
                    edges_uit += 1
        result += (p[node]/p_arrow(communities, p, alpha))*(edges_uit / graph.degree(node))
    
    for i in len(communities):
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
        p=np.matmul(A,p)        
        print(p)
        if np.allclose(previous,p, rtol = (1.e-5)/n): #moet deze error tolerance kleiner?
            return p.flatten().tolist()
    
    return p.flatten().tolist()




def calculate_HQ(communities, q):
    
    def fraction(q, i):
        teller = q[i]
        noemer = sum(q)
        return teller / noemer
    
    result = 0
    for i in len(communities):
        a = fraction(q, i)
        result += a*math.log(a, 2)
    
    return -1*result

def calculate_HPi(communities, q, p, i):
    
    p_sum = 0
    for b in communities[i]:
        p_sum += p[b]

    fraction1 = q[i]/(q[i]+p_sum)
    
    result = -1*fraction1*math.log(fraction1,2)
    
    for node in communities[i]:
        a = p[node]/(q[i]+p_sum)
        result -= a*math.log(a,2)
        
    return result


def LFR(n, t1, t2, mu, mincomsize, maxcomsize): #t1, t2 >1, 0<=mu<=1
    return nx.LFR_benchmark_graph(n, t1, t2, mu,min_degree=1 ,min_community = mincomsize, max_community = maxcomsize)

graph = LFR(100, 2.5, 2.5, 0.1,3, 20)
communities = {frozenset(graph.nodes[v]["community"]) for v in graph}
p = calculate_p(graph) # p wil je maar een keer berekenen, die is voor elke keuze van communities hetzelfde, en kost veel tijd

def map_equation(graph, communities, p):
    q = calculate_q(graph, communities, p)
    HQ = calculate_HQ(communities, q, p)
    result = sum(q)*HQ
    for i in range(len(communities)):
        p_a = p_arrow(communities, p, i)
        HPi = calculate_HPi(communities, q, p, i)
        result += (p_a*HPi)
    return result
        
