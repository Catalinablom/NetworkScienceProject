import matplotlib.pyplot as plt
import math
import json


def read_results():
    f = open('results\mu_results.tex', 'r')
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
    

def plot_mu_results(mus, comrange,num_runs, results):
    
# objective = 'mod'
# objective = 'map'

# kleuren = ['k','b','r','c','m','g']

# x = [0.1, 0.2, 0.3, 0.4]
# #x = list(eersteregel)
# kleur = 0
# for comrange in range(1,3):
#     y = []
#     for mu in x:  
#         y.append(math.sin(mu)+comrange)
#         #y.append(gemiddelde van juiste lijst in txt)
#     plt.plot(x, y, '-ok', label = 'Range community size: '+str(comrange), color = kleuren[kleur])
#     kleur += 1

# plt.xlabel('Mixing parameter')
# plt.ylabel('Normalized Mutual Information')
# #plt.title('Matplotlib Example')   
# plt.legend()
# plt.show() 
# #plt.savefig('plot_mu.png')

