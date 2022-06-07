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


# https://networkx.org/documentation/stable/reference/generated/networkx.generators.community.LFR_benchmark_graph.html
# exactly one of min_degree or average_degree must be specified.
# Bedenk welke waarden we willen invullen, welke parameters realistisch zijn
def LFR(n, t1, t2, mu, mincomsize, maxcomsize, tries): #t1, t2 >1, 0<=mu<=1
    try:
        graph = nx.LFR_benchmark_graph(n, t1, t2, mu, min_degree=1 ,min_community = mincomsize, max_community = maxcomsize)
    except:
        tries+=1
        print("tried and failed")
        graph, tries = LFR(n, t1, t2, mu, mincomsize, maxcomsize, tries)
    return graph, tries

# https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.quality.modularity.html
#communities in shape [{0, 1, 2}, {3, 4, 5}]

    
# Implement Louvain for modularity, je moet louvain wel zelf implementeren, anders kun je geen andere objective functie hebben
# Je wil modularity niet de functie pakken altijd, soms moet je alleen delta M hebben als je één node of één community verplaatst, dan is heel M uitrekenen veel langzamer dan delta M
            

def Louvain_map_firstround(original_G, G, communities, com_dic, p):
    
    #step 2
    improvement = True
    while improvement:
        # print("hier")
        test = []
        
        #shuffle node list
        nodes = list(G.nodes())
        random.shuffle(nodes)
        for node in nodes:
            
            current_map = map_equation2(original_G,communities, p)
            max_diff_M = 0
            neighbors = list(G.neighbors(node))
            random.shuffle(neighbors)
            for i in neighbors:
                if node != i: #snap neit waarom ie denkt dat een node een neighbour van zichzelf is maar prima
                    
                    # #make new possible partition
                    new_communities = copy.deepcopy(communities)
                    new_communities[i].update(communities[node])
                    new_communities[node]=set()

                    #calculate modularity for new partition
                    new_map = map_equation2(original_G,new_communities, p)
                    diff_map =  current_map - new_map 
                    
                    #save option that gives highest increase in modularity
                    if diff_map > max_diff_M:
                        best_option = i
                        max_diff_M = diff_map
                        
            
            if max_diff_M >0:
                
                #update edges in graph by contracting the communities into one node
                nx.contracted_nodes(G, best_option, node, self_loops=False)
                
                
                #update dic which keeps track of key: node, value: position of community it belongs to
                for j in communities[node]:
                    com_dic[j] = best_option
                    
                #update comunities list
                communities[best_option].update(communities[node])
                communities[node]=set()
                
                
        
            if max_diff_M == 0 : #if we imporove
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
    
    
    
    
def communities_to_vector(G,communities):
    t = [0]*G.number_of_nodes() 
    for community in range(len(communities)):
        for node in list(communities)[community]:
            t[node] = community
    return t

def print_communities(communities):
    for set in communities:
        if len(set) != 0:
            print(set)
            





# G = LFR(500, 2.5, 1.5, 0.1, 25, 100)
# # nx.draw(G)
# communities = {frozenset(G.nodes[v]["community"]) for v in G}
# p = calculate_p(G)
# print("Graph has been created \n")

# found_communities_map, _= Louvain_map(G, p)
# found_communities_mod, _ = Louvain_mod(G)


# #real_found_communities = nx_comm.louvain_communities(G)
# print("found mod", found_communities_mod)
# print("found map",found_communities_map)
# print("ground ",communities)
# # print("real_found_communities", real_found_communities)

            
# found_vector_map = communities_to_vector(G, found_communities_map)
# found_vector_mod = communities_to_vector(G, found_communities_mod)
# ground_vector = communities_to_vector(G, communities)
# # real_found_vector = communities_to_vector(G, real_found_communities)

# print("map eq results", norm_mutual_inf(found_vector_map,ground_vector))
# print("modularity result",norm_mutual_inf(found_vector_mod,ground_vector))
# # print(norm_mutual_inf(real_found_vector,ground_vector))


# "Er gaat wel nog wat fout met dat hij probeert een volle set te verplaatsen naar een lege, dat zou niet mogelijk moeten zijn"





