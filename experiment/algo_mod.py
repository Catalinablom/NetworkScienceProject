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
        # print("hier")
        test = []
        
        #shuffle node list
        nodes = list(G.nodes())
        random.shuffle(nodes)
        print("Running through all nodes")
        for node in nodes:
            current_loc_node = current_locations[node]
            current_mod = modularity(original_G,communities)
            max_diff_M = 0
            # M = modularity(G,communities)
            neighbors = list(G.neighbors(node))
            random.shuffle(neighbors)
            for i in neighbors:
                current_loc_i = current_locations[i]
                if current_loc_node != current_loc_i: #snap neit waarom ie denkt dat een node een neighbour van zichzelf is maar prima

                    #calculate modularity for new partition
                    # diff_M = calc_diff_M(original_G, communities[current_loc_node], communities[current_loc_i],OG_communities[node])
                    
                    
                    # #make new possible partition
                    new_communities = copy.deepcopy(communities)
                    new_communities[current_loc_i].update(OG_communities[node])
                    new_communities[current_loc_node].difference_update(OG_communities[node])
                    
                    # print("new\n",new_communities)

                    #calculate modularity for new partition
                    new_mod = modularity(original_G,new_communities)
                    diff_M = -( current_mod - new_mod)
                    
                    #save option that gives highest increase in modularity
                    if diff_M > max_diff_M:
                        loc_best_option = current_loc_i
                        max_diff_M = diff_M
                        
              
            
            if max_diff_M >0:  
                # print("max_diff_M", max_diff_M)      
                # #move node to best option
                # communities[current_community].remove(node)
                # communities[best_option].add(node)
                
                #update induced graph
                # G = nx.contracted_nodes(G, best_option, node, self_loops=False)
                
                #update dic which keeps track of key: node, value: position of community it belongs to
                #update community list
                communities[loc_best_option].update(OG_communities[node])
                communities[current_loc_node].difference_update(OG_communities[node])
                
                #update current locations
                current_locations[node] = loc_best_option
                
                
                #update dic which keeps track of key: node, value: position of community it belongs to
                for j in OG_communities[node]:
                    com_dic[j] = loc_best_option
                
                # print("here",communities)
                #print statemnt
                # print("updated to \n", communities)
                
        
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

#calculates diff in modularity from merging 2 communities
# def calc_diff_M(original_G, com_from, com_to):
#     diff = 0
#     m = original_G.number_of_edges()
#     for i in com_from:
#         for j in com_to:
#             ki=  len(list(original_G.neighbors(i)))
#             kj=  len(list(original_G.neighbors(j)))
#             if original_G.has_edge(i,j):
                
#                 diff += 1 - (ki*kj) / (2*m)
#             else: 
#                 diff += - (ki*kj) / (2*m)
#     diff = diff/ (2*m)
#     return diff


            
"Originale versie"
# def Louvain_modularity_firstround(original_G, G, communities, com_dic):
    
#     #step 2
#     print("One round of Louvain")
#     improvement = True
#     while improvement:
#         # print("hier")
#         test = []
        
#         #shuffle node list
#         nodes = list(G.nodes())
#         random.shuffle(nodes)
#         for node in nodes:
            
#             max_diff_M = 0
#             # M = modularity(G,communities)
#             neighbors = list(G.neighbors(node))
#             random.shuffle(neighbors)
#             for i in neighbors:
#                 if node != i: #snap neit waarom ie denkt dat een node een neighbour van zichzelf is maar prima
                    
#                     # #make new possible partition
#                     # new_communities = copy.deepcopy(communities)
#                     # new_communities[current_community].remove(node)
#                     # new_communities[possible_community].add(node)

#                     #calculate modularity for new partition
#                     diff_M = calc_diff_M(original_G, communities[node], communities[i])
                    
#                     #save option that gives highest increase in modularity
#                     if diff_M > max_diff_M:
#                         best_option = i
#                         max_diff_M = diff_M
                        
              
            
#             if max_diff_M >0:  
#                 # print("max_diff_M", max_diff_M)      
#                 # #move node to best option
#                 # communities[current_community].remove(node)
#                 # communities[best_option].add(node)
                
#                 #update induced graph
#                 # G = nx.contracted_nodes(G, best_option, node, self_loops=False)
                
#                 #update dic which keeps track of key: node, value: position of community it belongs to
#                 for j in communities[node]:
#                     com_dic[j] = best_option
                
#                 #move nodes to best option community
#                 # print("best option", best_option)
#                 # print("node", node)
#                 if best_option != node:
                    
#                     communities[best_option].update(communities[node])
#                     communities[node]=set()
                
#                 #print statemnt
#                 # print("updated to \n", communities)
                
        
#             if max_diff_M == 0 :
#                 test.append(False)
#             else:
#                 test.append(True)
                
#         improvement = any(test)
        
#     return communities, com_dic






# G, tries = LFR(20, 2, 1.05, 0.1, 2, 10, 0)
# found_communities_mod, _ = Louvain_mod(G)

# G = LFR(100, 2.5, 2.5, 0.1, 10, 30)
# nx.draw(G)
# communities = {frozenset(G.nodes[v]["community"]) for v in G}

# found_communities, _= Louvain_mod(G)
# real_found_communities = nx_comm.louvain_communities(G)
# print("found ",found_communities)
# print("ground ",communities)
# print("real_found_communities", real_found_communities)
            
# found_vector = communities_to_vector(G, found_communities)
# ground_vector = communities_to_vector(G, communities)
# real_found_vector = communities_to_vector(G, real_found_communities)

# print("wij",norm_mutual_inf(found_vector,ground_vector))
# print("zij",norm_mutual_inf(real_found_vector,ground_vector))





