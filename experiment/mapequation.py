# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:26:01 2022

@author: veerl
"""

import networkx as nx
import math

# TODO: vectoren p en q genereren

def q(graph, communities): 
    'vector of probabilities to go out of a certain community'
    # lengte is aantal communities
    return


def p(graph): 
    'Vector p of probabilities to be in a certain node'
    # met pagerank
    # lengte is aantal nodes
    return

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

p = p(graph) # p wil je maar een keer berekenen, die is voor elke keuze van communities hetzelfde, en kost veel tijd

def map_equation(graph, communities, p):
    q = q(graph, communities)
    HQ = HQ(communities, q, p)
    result = sum(q)*HQ
    for i in range(len(communities)):
        p_arrow = p_arrow(communities, p, i)
        HPi(communities, q, p, i)
        result += (p_arrow*HPi)
    return result
        
