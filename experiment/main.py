from algo_map import *
from algo_map import Louvain_map
from algo_mod import *
from algo_mod import Louvain_mod
from mapequation1 import *
import random
from normalized_mutual_information import *
import networkx as nx
import networkx.algorithms.community as nx_comm
import copy
import community as community_louvain
import random





def init():
    # random.seed(25)
    " We have to find a combination of parameter values that always is able to produce a graph"
    G = LFR(50, 2.5, 1.5, 0.2, 5, 20)
    # nx.draw(G)
    communities = {frozenset(G.nodes[v]["community"]) for v in G}
    p = calculate_p(G)
    return G, communities, p

def main():
    G, communities, p = init()
    print("Graph has been created \n")

    found_communities_map, _= Louvain_map(G, p)
    found_communities_mod, _ = Louvain_mod(G)


    #real_found_communities = nx_comm.louvain_communities(G)
    print("\nfound mod")
    print_communities(found_communities_mod)
    print("\nfound map")
    print_communities(found_communities_map)
    print("\nground ")
    print_communities(communities)
    
    # print("real_found_communities", real_found_communities)
                
    found_vector_map = communities_to_vector(G, found_communities_map)
    found_vector_mod = communities_to_vector(G, found_communities_mod)
    ground_vector = communities_to_vector(G, communities)
    #real_found_vector = communities_to_vector(G, real_found_communities)

    print("map eq results", norm_mutual_inf(found_vector_map,ground_vector))
    print("modularity result",norm_mutual_inf(found_vector_mod,ground_vector))

    # print(norm_mutual_inf(real_found_vector,ground_vector))


    "Er gaat wel nog wat fout met dat hij probeert een volle set te verplaatsen naar een lege, dat zou niet mogelijk moeten zijn"

main()