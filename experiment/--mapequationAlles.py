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





def p_arrow(communities, p, i): # p_arrow as in paper, without the q term
    result = 0
    if len(list(communities)[i])==0:
            return 0
    for node in list(communities)[i]:
        result += p[node]
    return result


def calculate_q(graph, communities, p): 
    'vector of probabilities to go out of a certain community'
    q = []
    # lengte is aantal communities
    def calculate_qi(alpha):
        if len(list(communities[alpha]))==0:
            return 0
        result = 0
        for node in list(communities[alpha]):
            edges_uit=0
            neighbours = list(graph.neighbors(node))
            for neighbour in neighbours: #zorgen dat er geen self loops zijn
                if neighbour not in list(communities[alpha]):
                    edges_uit += 1
            result += (p[node])*(edges_uit / graph.degree[node])
        return p_arrow(communities, p, alpha)*result
        #return result
    
    for i in range(len(communities)):
        qi = calculate_qi(i)
        q.append(qi)  
    #print('Dit is q:', q)  
    #print('som q:',sum(q))
    return q

def calculate_q2(graph, communities, p): 
    'vector of probabilities to go out of a certain community'
    q = []
    # lengte is aantal communities
    def calculate_qi(alpha):
        if len(list(communities)[alpha])==0:
            return 0
        result = 0
        edges_uit=0
        degrees = 0
        for node in list(communities)[alpha]:
            degrees += graph.degree[node]
            for neighbour in list(graph.neighbors(node)):
                if neighbour not in list(communities)[alpha]:
                    edges_uit += 1
        result = edges_uit / degrees
        
        return p_arrow(communities, p, alpha) * result
    
    for i in range(len(communities)):
        qi = calculate_qi(i)
        q.append(qi)  
    #print('\n\nDit is q2:', q)  
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
        if np.allclose(previous,p, rtol = (1.e-5)/n): 
            return p.flatten().tolist()
    
    return p.flatten().tolist()




def calculate_HQ(communities, q):
    
    def fraction12(q, i):
        teller = q[i]
        noemer = sum(q)
        if noemer == 0 :
            return 0
        return teller / noemer
    
    
    result = 0
    for i in range(len(communities)):
        a = fraction12(q, i)
        if a == 0:
            result += 0
        else:
            result += a*math.log(a, 2)
    
    return -1*result

def calculate_HPi(communities, q, p, i):
    
    p_sum = p_arrow(communities,p,  i)

    if (q[i]+p_sum) == 0:
        fraction1 = 0
    else:
        fraction1 = q[i]/(q[i]+p_sum)
    
    if fraction1 == 0:
        result = 0
    else:
        result = -1*fraction1*math.log(fraction1,2)
    
    for node in list(communities)[i]:
        if q[i]+p_sum == 0:
            a = 0
        else:
            a = p[node]/(q[i]+p_sum)
        
        if a == 0:
            result = result
        else:
            result = result - a*math.log(a,2)
        
    return result



def map_equation1(graph, communities, p):
    q = calculate_q2(graph, communities, p)
    HQ = calculate_HQ(communities, q)
    result = sum(q)*HQ
    for i in range(len(communities)):
        #p_a = p_arrow(communities, p, i)
        p_a = p_arrow(communities, p, i)+q[i]
        HPi = calculate_HPi(communities, q, p, i)
        result += (p_a*HPi)
    return result
        
        

# print*map_equation(graph,communities,p)


'Tweede manier voor map_eq, equation (4) uit paper'

def a_log_a(a):
    if a == 0:
        return 0
    else:
        return a*math.log(a,2)
    
def map_equation2(graph, communities, p):
    q = calculate_q2(graph, communities, p)
    # print(communities)
    result = a_log_a(sum(q))
    
    term = 0
    for i in range(len(communities)):
        term += a_log_a(q[i])
    
    term2 = 0
    for alpha in list(graph.nodes()):
        term2 += a_log_a(p[alpha])
    
    term3 = 0
    for i in range(len(communities)):
        a = q[i]+ p_arrow(communities, p, i)
        #a = p_arrow(communities, p, i)
        term3 += a_log_a(a)

    result += -2*term -term2 + term3
    
    return result

# L geeft een hogere waarde, heeft met q te maken. Als sum(q) hoger is dan is L ook hoger tov map_eq
# als sum(q) bijna 0, dan geven ze bijna dezelfde waarde, en als sum(q)=0 dan zijn ze gelijk
# graph = LFR(50, 2.5, 2.5, 0.3,10, 25)
# communities = list({frozenset(graph.nodes[v]["community"]) for v in graph})
# # print(communities)
# p = calculate_p(graph) # p wil je maar een keer berekenen, die is voor elke keuze van communities hetzelfde, en kost veel tijd

# # print("\n\n compprob",comprob)


# print("som p", sum(p))
# '''
# q1 = calculate_q(graph,communities,p)
# print('Dit is q1:', q1)
# print('/n Som q:', sum(q1))
# '''
# q2 = calculate_q2(graph,communities,p)
# print('Dit is q2:', q2)
# print('/n Som q:', sum(q2))

# #q2 = calculate_q2(graph,communities,p)
# print('mapeq1:', map_equation1(graph, communities, p))
# print('mapeq2:', map_equation2(graph, communities, p))