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
import numpy as np
from plotmu import * 

def main(mus, comsizes, num_runs, n):
    mus = [0.2]
    # mus=[0.1]
    # (3*mult,5*mult),(mult, 5*mult), (mult, 6*mult),
    a= 5
    b = 25
    c= 10
    # comsizes = [(a,b),(2*a,2*b),(3*a,3*b),(4*a,4*b), (a,2*b), (a,3*b),(a,4*b),(a+c,b+c),(a+2*c,b+2*c),(a+3*c,b+3*c)]
    comsizes = []
    #for i in range(1,17):
    #    comsizes.append((round(i*a),round(i*b)))
    #for i in range(2,17):
    #     comsizes.append((a,i*b))
    'Eerste'
    for i in range(0, 6):
        comsizes.append((a+i*c, b+i*c))
    d = 2
    for i in range(1,8):
        comsizes.append((a+i*d, b+i*d))
    e = 4
    for i in range(1,8):
        comsizes.append((a, b+i*e))
        
    'Tweede'
    
    # comsizes = [(a,b)]
    num_runs = 2
    results = {}
    tic = time.perf_counter()
    
    for mu in mus:
        for comsize_num in range(len(comsizes)):
            print(mu, comsize_num)
            comsizeL, comsizeR = comsizes[comsize_num]
            map_results =[]
            mod_results = []
            # realmod_results = []
            for i in range(num_runs):
                #generate graph
                print("Creating graph")
                G, tries = LFR(n, 2.8, 1.8, mu, comsizeL, comsizeR, 0)
                print("Graph created after ",tries," tries")
                p = calculate_p(G)
                
                #find ground communities and avg community size
                communities = {frozenset(G.nodes[v]["community"]) for v in G}
                
                num_com = len(communities)
                sizes = []
                for community in communities:
                    sizes.append(len(community))
                results[(mu, comsize_num,i)]= sizes
                    
                #find diff communities
                found_communities_map, _= Louvain_map(G, p)
                found_communities_mod, _ = Louvain_mod(G)
                
                #convert to vector
                found_vector_map = communities_to_vector(G, found_communities_map)
                found_vector_mod = communities_to_vector(G, found_communities_mod)
                ground_vector = communities_to_vector(G, communities)
                
                #calculcate normalized mutual information
                map_results.append(norm_mutual_inf(found_vector_map,ground_vector))
                mod_results.append(norm_mutual_inf(found_vector_mod,ground_vector))
                
                
                
            results[(mu,comsize_num,"map")] = map_results
            results[(mu,comsize_num,"mod")] = mod_results


    toc = time.perf_counter()
    print(f"Total run in in {toc - tic:0.4f} seconds") 
    save_results((mus, comsizes,num_runs),results)
    
    
"Function that saves results to folder results"
def save_results(params,results):
    #save results to results\mu_results.tex
    mus, comsizes,num_runs = params
    
    "Write your own path here to read results"
    f = open(r"c:\Users\veerl\OneDrive\Documenten\Mathematical Sciences\Network Science\git\NetworkScienceProject\experiment\results\mu_results.tex", 'w')
    #f = open("results\mu_results.tex", 'w')
    
    
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
        #f.write(str(mu)+ ","+ str(comsize) + ","+ str(name))
        f.write(str(mu)+ ","+ str(comsize+31) + ","+ str(name))
        f.write(":")
        for result in results[key]:
            f.write(str(result)+ ',')
        f.write("\n")
    f.close()


random.seed(5)

"Uncomment the following code and run main.py to plot our results for different values of mu."
mus = [0.05,0.1,0.15,0.2,0.25,0.3]
n = 200
comsizes = [(4, 20),(6, 30),(8, 40)]
num_runs = 10
main(mus, comsizes, num_runs, n)
mus, comrange,num_runs, results = read_results()
plot_mu_results_map(mus, comrange,num_runs, results)
plot_mu_results_mod(mus, comrange,num_runs, results)

"Uncomment the following code and run main.py to run our experiment and plot the results."
n = 500
mus = [0.25]
num_runs = 2 
main(mus, comsizes, num_runs, n)
