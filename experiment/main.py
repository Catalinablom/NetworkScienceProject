from re import A
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
#import community as community_louvain
import random
import time

def init():
    # random.seed(25)
    " We have to find a combination of parameter values that always is able to produce a graph"
    G, tries = LFR(50, 2, 1.05, 0.1, 10, 25, 0)
    print(tries)
    # nx.draw(G)
    communities = {frozenset(G.nodes[v]["community"]) for v in G}
    p = calculate_p(G)
    return G, communities, p

def main():
    mult = 20
    mus = [0.05,0.1,0.15,0.2,0.25,0.3]
    # mus=[0.1]
    comsizes = [(3*mult,5*mult),(mult, 5*mult), (mult, 6*mult)]
    num_runs = 2
    results = {}
    
    for mu in mus:
        for comsize_num in range(len(comsizes)):
            print(mu, comsize_num)
            comsizeL, comsizeR = comsizes[comsize_num]
            map_results =[]
            mod_results = []
            realmod_results = []
            for i in range(num_runs):
                #generate graph
                print("Creating graph")
                G, tries = LFR(10*mult, 2, 1.05, mu, comsizeL, comsizeR, 0)
                print("Graph created after ",tries," tries")
                p = calculate_p(G)
                
                #find ground communities
                communities = {frozenset(G.nodes[v]["community"]) for v in G}
                
                #find diff communities
                tic = time.perf_counter()
                found_communities_map, _= Louvain_map(G, p)
                toc = time.perf_counter()
                print(f"map solution found in {toc - tic:0.4f} seconds")
                found_communities_mod, _ = Louvain_mod(G)
                real_found_communities = nx_comm.louvain_communities(G)
                
                #convert to vector
                found_vector_map = communities_to_vector(G, found_communities_map)
                found_vector_mod = communities_to_vector(G, found_communities_mod)
                ground_vector = communities_to_vector(G, communities)
                real_found = communities_to_vector(G,real_found_communities)
                
                #calculcate normalized mutual information
                map_results.append(norm_mutual_inf(found_vector_map,ground_vector))
                mod_results.append(norm_mutual_inf(found_vector_mod,ground_vector))
                realmod_results.append(norm_mutual_inf(real_found,ground_vector))
                
            results[(mu,comsize_num,"map")] = map_results
            results[(mu,comsize_num,"mod")] = mod_results
            results[(mu,comsize_num,"realmod")] = realmod_results
            

        
    save_results((mus, comsizes,num_runs),results)


    "Er gaat wel nog wat fout met dat hij probeert een volle set te verplaatsen naar een lege, dat zou niet mogelijk moeten zijn"

def save_results(params,results):
    mus, comsizes,num_runs = params
    f = open("results\mu_results.tex", 'w')
    
    for mu in mus:
        f.write(str(mu)+",")
    f.write("\n")
    
    for comsize in comsizes:
        l,r = comsize
        f.write(str(l)+","+str(r)+ ",")
    f.write("\n")
    
    f.write(str(num_runs)+"\n")
    
    for key in results:
        mu , comsize, name = key
        f.write(str(mu)+ ","+ str(comsize) + ","+ str(name))
        f.write(":")
        for result in results[key]:
            f.write(str(result)+ ',')
        f.write("\n")
    f.close()


random.seed(25)
main()

