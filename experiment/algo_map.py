from ast import Or
# from selectors import EpollSelector
from normalized_mutual_information import *
from mapequation1 import *
from algo_mod import *
import networkx as nx
import networkx.algorithms.community as nx_comm
import copy
#import community as community_louvain
import random
from helper import *
        
"One round of louvain with map equation"
def Louvain_map_firstround(original_G, G, communities, com_dic, p):
    
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
        count = 0
        print("Running through all nodes")
        #nodes are index of OG_communities
        for node in nodes:
            current_loc_node = current_locations[node]
            current_map = map_equation2(original_G,communities, p)
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
                    new_map = map_equation2(original_G,new_communities, p)
                    diff_map =  current_map - new_map 
                    
                    #save option that gives highest increase in modularity
                    if diff_map > max_diff_M:
                        loc_best_option = current_loc_i
                        max_diff_M = diff_map
                        
            count +=1 
            if max_diff_M >0:
                
                #update community list
                communities[loc_best_option].update(OG_communities[node])
                communities[current_loc_node].difference_update(OG_communities[node])
                
                #update current locations
                current_locations[node] = loc_best_option
                
                
                #update dic which keeps track of key: node, value: position of community it belongs to
                for j in OG_communities[node]:
                    com_dic[j] = loc_best_option
                    
        
        
            if max_diff_M == 0 : #if we imporove
                test.append(False)
            else:
                test.append(True)
            
        #check if there was improvement    
        improvement = any(test)
        
    return communities, com_dic

    

"Main louvain algorithm with map equation"

def Louvain_map(original_G, p):
    G = copy.deepcopy(original_G)
    #step 1 : initliaze communities and modularity
    communities = [{i} for i in range(G.number_of_nodes())]
    
    #create dic which keeps track of key: node, value: position of community it belongs to
    com_dic = generate_com_dic(communities)
    
    improvement =1
    previous_map= map_equation2(G, communities, p)
    while improvement > 0:
        #run first round
        communities, com_dic = Louvain_map_firstround(original_G,G, communities, com_dic, p)
        
        #calculate new modularity
        current_map = map_equation2(original_G, communities, p)
        improvement =  previous_map - current_map  #switch because we minimalize
        G = induced_graph(com_dic,G)
        previous_map = current_map
    
    
    return communities, com_dic
    
    
    
    





