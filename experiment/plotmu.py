import matplotlib.pyplot as plt
import math
import json


def read_results():
    "Write your own path here to read results"
    f = open(r"c:\Users\veerl\OneDrive\Documenten\Mathematical Sciences\Network Science\git\NetworkScienceProject\experiment\results\mu_results.tex", 'r')
    #f = open('results\mu_results.tex', 'r')
    lines = f.readlines()

    #find mus
    mus1 = list(lines[0].split(','))
    mus1.pop()
    print(mus1)
    mus= [float(mu) for mu in mus1]
    
    #find com sizes
    comrangelist = lines[1].split(',')
    comrangelist.pop()
    comrange = [[int(comrangelist[i]), int(comrangelist[i+1])] for i in range(0,len(comrangelist), 2)]
    
    #find num_runs
    num_runs = int(lines[2])

    #find results
    results ={}
    for line in lines[3:]:
        linessplit = line.split(":")
        input_string = linessplit[0].split(",")

        output_string = linessplit[1].split(",")
        output_string.pop()
        
        input = (float(input_string[0]), float(input_string[1]), input_string[2])
        output = [float(x) for x in output_string]
        
        results[input] = output
    
    f.close()
        
    return mus, comrange,num_runs, results
    
# make a plot of normalized mutual information against mixing parameter mu for modularity, different lines corrsponding to different graphs are plot
def plot_mu_results_mod(mus, comrange,num_runs, results):
    kleuren = ['k','b','r','c','m','g']
    kleur = 0
    for comtype in range(len(comrange)):
        y =[]
        for mu in mus:
            resultlist = results[(mu,comtype,'mod')]
            val = sum(resultlist)/num_runs
            y.append(val)
        plt.plot(mus, y, '-ok', label = 'Range community size: '+str(comrange[comtype]), color = kleuren[kleur])
        kleur += 1
    
    plt.xlabel('Mixing parameter')
    plt.ylabel('Normalized Mutual Information')
    plt.title('Objective function: modularity')   
    plt.legend()
    plt.ylim(0,1)
    plt.savefig('plot_mu_mod.png') 
    plt.show() 
    
# make a plot of normalized mutual information against mixing parameter mu for map equation, different lines corrsponding to different graphs are plot
def plot_mu_results_map(mus, comrange,num_runs, results):
    kleuren = ['k','b','r','c','m','g']
    kleur = 0
    for comtype in range(len(comrange)):
        y =[]
        for mu in mus:
            resultlist = results[(mu,comtype, 'map')]
            val = sum(resultlist)/num_runs
            y.append(val)
        plt.plot(mus, y, '-ok', label = 'Range community size: '+str(comrange[comtype]), color = kleuren[kleur])
        kleur += 1
    
    plt.xlabel('Mixing parameter')
    plt.ylabel('Normalized Mutual Information')
    plt.title('Objective function: map equation')   
    plt.legend()
    plt.ylim(0,1)
    plt.savefig('plot_mu_map.png')
    plt.show() 
    
# read results and make the corresponding plots
mus, comrange,num_runs, results = read_results()
plot_mu_results_map(mus, comrange,num_runs, results)
plot_mu_results_mod(mus, comrange,num_runs, results)
            

