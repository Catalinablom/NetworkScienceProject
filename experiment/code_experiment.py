# -*- coding: utf-8 -*-
"""
Created on Mon May 23 13:39:44 2022

@author: veerl
"""

from ast import Or
# from selectors import EpollSelector
from normalized_mutual_information import *
import networkx as nx
import networkx.algorithms.community as nx_comm
import copy
import community as community_louvain

# https://networkx.org/documentation/stable/reference/generated/networkx.generators.community.LFR_benchmark_graph.html
# exactly one of min_degree or average_degree must be specified.
# Bedenk welke waarden we willen invullen, welke parameters realistisch zijn
def LFR(n, t1, t2, mu, mincomsize, maxcomsize): #t1, t2 >1, 0<=mu<=1
    return nx.LFR_benchmark_graph(n, t1, t2, mu,min_degree=1 ,min_community = mincomsize, max_community = maxcomsize)

G = LFR(40, 2.5, 2.5, 0.3,3, 7)
nx.draw(G)
communities = {frozenset(G.nodes[v]["community"]) for v in G}
print(communities) 

# https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.quality.modularity.html
#communities in shape [{0, 1, 2}, {3, 4, 5}]
def modularity(G, communities):
    return nx_comm.modularity(G, communities)
    
# Implement Louvain for modularity, je moet louvain wel zelf implementeren, anders kun je geen andere objective functie hebben
# Je wil modularity niet de functie pakken altijd, soms moet je alleen delta M hebben als je één node of één community verplaatst, dan is heel M uitrekenen veel langzamer dan delta M

def calc_diff_M(original_G, com_from, com_to):
    diff = 0
    m = original_G.number_of_edges()
    for i in com_from:
        for j in com_to:
            ki=  len(list(original_G.neighbors(i)))
            kj=  len(list(original_G.neighbors(j)))
            if original_G.has_edge(i,j):
                
                diff += 1 - (ki*kj) / (2*m)
            else: 
                diff += - (ki*kj) / (2*m)
    diff = diff/ (2*m)
    return diff
            

def Louvain_modularity_firstround(original_G, G, communities, com_dic):
    
    #step 2
    improvement = True
    while improvement:
        print("hier")
        test = []
        for node in list(G.nodes()):
            
            max_diff_M = 0
            # M = modularity(G,communities)
            for i in G.neighbors(node):
                if node != i: #snap neit waarom ie denkt dat een node een neighbour van zichzelf is maar prima
                    
                    # #make new possible partition
                    # new_communities = copy.deepcopy(communities)
                    # new_communities[current_community].remove(node)
                    # new_communities[possible_community].add(node)

                    #calculate modularity for new partition
                    diff_M = calc_diff_M(original_G, communities[node], communities[i])
                    
                    #save option that gives highest increase in modularity
                    if diff_M > max_diff_M:
                        best_option = i
                        max_diff_M = diff_M
                        
              
            
            if max_diff_M >0:  
                print("max_diff_M", max_diff_M)      
                # #move node to best option
                # communities[current_community].remove(node)
                # communities[best_option].add(node)
                
                #update dic which keeps track of key: node, value: position of community it belongs to
                for j in communities[node]:
                    com_dic[j] = best_option
                
                #move nodes to best option community
                # print("best option", best_option)
                # print("node", node)
                if best_option != node:
                    
                    communities[best_option].update(communities[node])
                    communities[node]={}
                
                #print statemnt
                # print("updated to \n", communities)
                
        
            if max_diff_M == 0 :
                test.append(False)
            else:
                test.append(True)
                
        improvement = any(test)
        
    return communities, com_dic

#generates dictionary with key : node, value: community it belongs to
def generate_com_dic(communities):
    num_communities = len(communities)
    com_dic = {}
    for i in range(num_communities):
        for node in communities[i]:
            com_dic[node]=i
            
    return com_dic
    


#compresses each community into one node
def induced_graph(com_dic, graph):
    "inspiration from https://github.com/taynaud/python-louvain/blob/master/community/community_louvain.py"
    
    #nodecom_to_gencom keeps tracks of which nodes are actually in communities compressed to nodes
    #is a dic with key: node name, value: set of nodes
    ret = nx.Graph()
    ret.add_nodes_from(com_dic.values())

    for node1, node2 in graph.edges():
        com1 = com_dic[node1]
        com2 = com_dic[node2]
        ret.add_edge(com1, com2)

    return ret

def Louvain_mod(original_G):
    G = original_G
    #step 1 : initliaze communities and modularity
    communities = [{i} for i in range(G.number_of_nodes())]
    
    
    #create dic which keeps track of key: node, value: position of community it belongs to
    com_dic = generate_com_dic(communities)
    
    
    
    improvement =1
    previous_mod= modularity(G, communities)
    while improvement > 0:
        #run first round
        communities, com_dic = Louvain_modularity_firstround(original_G,G, communities, com_dic)
        
        #calculate new modularity
        current_mod = modularity(original_G, communities)
        improvement =  current_mod - previous_mod 
        G = induced_graph(com_dic,G)
        previous_mod = current_mod
    
    
    return communities, com_dic
    
    
    
    
def communities_to_vector(G,communities):
    t = [0]*G.number_of_nodes() 
    for community in range(len(communities)):
        for node in list(communities)[community]:
            t[node] = community
    return t

found_communities, _= Louvain_mod(G)
real_found_communities = partition = community_louvain.best_partition(G)
print("found ",found_communities)
print("ground ",communities)
print("real_found_communities", real_found_communities)
            
found_vector = communities_to_vector(G, found_communities)
ground_vector = communities_to_vector(G, communities)

print(norm_mutual_inf(found_vector,ground_vector))













    
# # implement Louvain for map equation
# def Louvain_map_eq(G): # minimize map equation instead of maximize modularity
#     return

# # implement map equation
# def entropy(Q):
#     return 
# def p(g):
#     return
# def map_equation(G, communities): 
#     q = #fraction of time that the random walk spends moving between communities 
#     P_g = 
#     H_Q = 
#     H_P_g = 
#     som = 0
#     for g in communities:
#         som = som + p(g)*entropy(P_g)
#     return q * entropy(Q) + som
