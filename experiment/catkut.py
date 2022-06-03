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


# def calculate_q(graph, communities, p): 
#     'vector of probabilities to go out of a certain community'
#     q = []
#     # lengte is aantal communities
#     def calculate_qi(alpha):
#         if len(list(communities[alpha]))==0:
#             return 0
#         result = 0
#         current_com = list(communities[alpha])
#         for node in list(communities[alpha]):
#             edges_uit=0
#             neighbours = list(graph.neighbors(node))
#             for neighbour in neighbours: #zorgen dat er geen self loops zijn
#                 if neighbour not in list(communities[alpha]):
#                     edges_uit += 1
#             a=(p[node])*(edges_uit / graph.degree(node))
#             # print("erbij",a)
#             kans_leave = edges_uit / graph.degree(node)
#             result += (p[node])*(edges_uit / graph.degree(node))
#         return result
    
#     for i in range(len(communities)):
#         qi = calculate_qi(i)
#         q.append(qi)  
#     print('Dit is q:', q)  
#     print(sum(q))
#     return q

def calculate_q(graph,communities,p):
    q =[]
    for i  in range(len(communities)):
        
        result = 0
        community = list(communities[i])
        prob_com = p_arrow(communities, p, i)
        for node in community:
            prob_node = p[node]/prob_com
            edges_uit = 0
            edges_tot = 0
            neighbours = list(graph.neighbors(node))
            for neighbor in neighbours:
                edges_tot +=1
                if neighbor not in community:
                    edges_uit+=1
            result+= prob_node * (edges_uit /edges_tot)
        q.append(prob_com*result)
                
            
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
            degrees += graph.degree(node)
            for neighbour in graph.neighbors(node):
                if neighbour not in list(communities)[alpha]:
                    edges_uit += 1
        result = edges_uit / degrees
        
        return p_arrow(communities, p, alpha) * result
    
    for i in range(len(communities)):
        qi = calculate_qi(i)
        q.append(qi)  
    print('\n\nDit is q2:', q)  
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
        # if np.allclose(previous,p, rtol = (1.e-5)/n): 
        #       p = normalize(p, axis=0, norm='l1')
        #     return p.flatten().tolist()
        
    p = normalize(p, axis=0, norm='l1')
    
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
        p_a = p_arrow(communities, p, i)
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
    q = calculate_q(graph, communities, p)
    # print(communities)
    result = a_log_a(sum(q))
    
    term = 0
    for i in range(len(communities)):
        term += a_log_a(q[i])
    
    term2 = 0
    for alpha in range(graph.number_of_nodes()):
        term2 += a_log_a(p[alpha])
    
    term3 = 0
    for i in range(len(communities)):
        a = q[i]+ p_arrow(communities, p, i)
        term3 += a_log_a(a)

    result += -2*term -term2 + term3
    
    return result


#create own graph
ret = nx.Graph()
ret.add_nodes_from([0,1,2,3,4,5,6])
ret.add_edge(0,1)
ret.add_edge(1,5)
ret.add_edge(1,4)
ret.add_edge(2,3)
ret.add_edge(2,6)
ret.add_edge(2,5)
ret.add_edge(4,5)
ret.add_edge(5,6)
# graph = ret

communities = [{1,2,4,5},{3,6}]
p = [1/7,1/7,1/7,1/7,1/7,1/7,1/7]




# L geeft een hogere waarde, heeft met q te maken. Als sum(q) hoger is dan is L ook hoger tov map_eq
# als sum(q) bijna 0, dan geven ze bijna dezelfde waarde, en als sum(q)=0 dan zijn ze gelijk
graph = LFR(50, 2.5, 2.5, 0.3,10, 25)
communities = list({frozenset(graph.nodes[v]["community"]) for v in graph})
print(communities)
# print(communities)
p = calculate_p(graph) # p wil je maar een keer berekenen, die is voor elke keuze van communities hetzelfde, en kost veel tijd
for i in range(len(communities)):
    print(communities[i])
    print(p_arrow(communities, p, i))
print("som p", sum(p))

print("self loops", list(nx.selfloop_edges(graph)))
q1 = calculate_q(graph,communities,p)
print(sum(q1))
q2 = calculate_q2(graph,communities,p)
print(sum(q2))
# print('mapeq1:', map_equation1(graph, communities, p))
# print('mapeq2:', map_equation2(graph, communities, p))