# -*- coding: utf-8 -*-


from ast import Or
# from selectors import EpollSelector
from normalized_mutual_information import *
import networkx as nx
import networkx.algorithms.community as nx_comm
import copy
#import community as community_louvain
import random
from helper import *
# from algo_map import LFR

"One round of louvain with modularity"

def Louvain_modularity_firstround(original_G, G, communities, com_dic):
    
    #step 2
    print("One round of Louvain")
    improvement = True
    
    OG_communities = copy.deepcopy(communities)
    current_locations = {}
    for node in G.nodes():
        current_locations[node] = node
        
    while improvement:
        test = []
        
        #shuffle node list
        nodes = list(G.nodes())
        random.shuffle(nodes)
        print("Running through all nodes")
        for node in nodes:
            current_loc_node = current_locations[node]
            current_mod = modularity(original_G,communities)
            max_diff_M = 0
            neighbors = list(G.neighbors(node))
            random.shuffle(neighbors)
            for i in neighbors:
                current_loc_i = current_locations[i]
                if current_loc_node != current_loc_i:
                    
                    
                    # #make new possible partition
                    new_communities = copy.deepcopy(communities)
                    new_communities[current_loc_i].update(OG_communities[node])
                    new_communities[current_loc_node].difference_update(OG_communities[node])
                    

                    #calculate modularity for new partition
                    new_mod = modularity(original_G,new_communities)
                    diff_M = -( current_mod - new_mod)
                    
                    #save option that gives highest increase in modularity
                    if diff_M > max_diff_M:
                        loc_best_option = current_loc_i
                        max_diff_M = diff_M
                        
              
            
            if max_diff_M >0:  
                #update community list
                communities[loc_best_option].update(OG_communities[node])
                communities[current_loc_node].difference_update(OG_communities[node])
                
                #update current locations
                current_locations[node] = loc_best_option
                
                
                #update dic which keeps track of key: node, value: position of community it belongs to
                for j in OG_communities[node]:
                    com_dic[j] = loc_best_option
                
        
            if max_diff_M == 0 :
                test.append(False)
            else:
                test.append(True)
        
        #check if there was improvement    
        improvement = any(test)
        
    return communities, com_dic



"Main louvain algorithm with modularity"

def Louvain_mod(original_G):
    G = copy.deepcopy(original_G)
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
    
    
    
"Calculates the difference in modularity from moving a set of vertices to another community"
#this function was not used in our implementation, but may be useful for further research

def calc_diff_M(original_G, com_from, com_to, moved):
    diff = 0
    m = original_G.number_of_edges()
    # com_from.difference_update(moved)
    sep_com_from = com_from - moved
    for i in moved:
        #new edges within the community
        for j in com_to:

            ki=  len(list(original_G.neighbors(i)))
            kj=  len(list(original_G.neighbors(j)))
            if original_G.has_edge(i,j):
                
                diff += 1 - (ki*kj) / (2*m)
            else: 
                diff += - (ki*kj) / (2*m)
          
        #edges that are no longer within a community      
        for l in sep_com_from:

            ki=  len(list(original_G.neighbors(i)))
            kl=  len(list(original_G.neighbors(l)))
            if original_G.has_edge(i,l):
                diff -= 1 - (ki*kl) / (2*m)
            else: 
                diff -=  -(ki*kl) / (2*m)
                
    
    diff = diff/ (2*m)
    return diff


