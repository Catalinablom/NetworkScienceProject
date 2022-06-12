from ast import Or
# from selectors import EpollSelector
from normalized_mutual_information import *
import networkx as nx
import networkx.algorithms.community as nx_comm
import copy
#import community as community_louvain
import random


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

    ret = nx.Graph()
    ret.add_nodes_from(com_dic.values())

    for node1, node2 in graph.edges():
        com1 = com_dic[node1]
        com2 = com_dic[node2]
        ret.add_edge(com1, com2)

    return ret

#calculate modularity of a graph and communities
def modularity(G, communities):
    return nx_comm.modularity(G, communities)

# https://networkx.org/documentation/stable/reference/generated/networkx.generators.community.LFR_benchmark_graph.html
# exactly one of min_degree or average_degree must be specified.
# Bedenk welke waarden we willen invullen, welke parameters realistisch zijn
"Function that tries to generate an LFR benchmark graph (at most 100 times)"
def LFR(n, t1, t2, mu, mincomsize, maxcomsize, tries): #t1, t2 >1, 0<=mu<=1
    if tries<100:
        try:
            
            graph = nx.LFR_benchmark_graph(n, t1, t2, mu, average_degree=5 ,min_community = mincomsize, max_community = maxcomsize)
        except:
            tries+=1
            print("tried and failed")
            graph, tries = LFR(n, t1, t2, mu, mincomsize, maxcomsize, tries)
        return graph, tries
    else:
        return None
   
#print communities (leaving out empty sets) 
def print_communities(communities):
    for set in communities:
        if len(set) != 0:
            print(set)
            
#converts communities to vector so mutual information can be calculated       
def communities_to_vector(G,communities):
    t = [0]*G.number_of_nodes() 
    for community in range(len(communities)):
        for node in list(communities)[community]:
            t[node] = community
    return t