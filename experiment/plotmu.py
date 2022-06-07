import matplotlib.pyplot as plt
import math

#f = open('file1.txt', 'r')
lines = f.readlines()
mus = list(lines[0].split(','))
comrangelist = lines[1].split(',')
comrange = [[comrangelist[i], comrangelist[i+1]] for i in range(len(comrangelist), 2)]
lines[2]

for line in lines:
    line.split(':')
    
    

objective = 'mod'
objective = 'map'

kleuren = ['k','b','r','c','m','g']

x = [0.1, 0.2, 0.3, 0.4]
#x = list(eersteregel)
kleur = 0
for comrange in range(1,3):
    y = []
    for mu in x:  
        y.append(math.sin(mu)+comrange)
        #y.append(gemiddelde van juiste lijst in txt)
    plt.plot(x, y, '-ok', label = 'Range community size: '+str(comrange), color = kleuren[kleur])
    kleur += 1

plt.xlabel('Mixing parameter')
plt.ylabel('Normalized Mutual Information')
#plt.title('Matplotlib Example')   
plt.legend()
plt.show() 
#plt.savefig('plot_mu.png')

f.close()