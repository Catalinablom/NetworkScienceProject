from algo_map import *
from algo_map import Louvain_map
from algo_mod import *
from algo_mod import Louvain_mod
from mapequation import *
import random




def init(n,tau1,tau2,mu,min_community,max_community):
    # random.seed(25)
    " We have to find a combination of parameter values that always is able to produce a graph"
    G = nx.LFR_benchmark_graph(n, tau1, tau2, mu, average_degree= 20,max_degree = 50, min_community = min_community, max_community = max_community)
    # nx.draw(G)
    communities = {frozenset(G.nodes[v]["community"]) for v in G}
    p = calculate_p(G)
    return G, communities, p

def main():
    G, communities, p = init(n=1000, tau1=2.5, tau2=2.5, mu=0.1, min_community=20,max_community=100)
    print("Graph has been created \n")

    found_communities_map, _= Louvain_map(G, p)
    found_communities_mod, _ = Louvain_mod(G)


    #real_found_communities = nx_comm.louvain_communities(G)
    print("found mod", found_communities_mod)
    print("found map",found_communities_map)
    print("ground ",communities)
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