# NetworkScienceProject
This is a project for the course Network Science on community detection.
The goal of this project is to experiment with how the Louvain algorithm performs objective to modularity or the map equation on graphs with different ranges of community sizes. For a more extensive explanation of this project, we would like to refer to the corresponding paper.

For this project we implemented the Louvain algorithm with objective function modularity in algo_mod.py (which also includes the function to generate LFR benchmark graphs) and the Louvain algorithm with objective function map equation in algo_map.py. The map equation itself is implemented in mapequation1.py. Furthermore, to determine the performance of the Louvain algorithm objective to either modularity or map equation, we implemented the normalized mutual information measure in normalized_mutual_information.py. Now, the file main.py combines all the files above and saves results (normalized mutual information values of obtained community divisions) in the map results. In main.py, one can adjust which values of the mixing parameter mu to use, which community size ranges to consider and the number of runs. 
After obtaining results trough the main file, one can visualise them with the file plotresults.py. The file plotmu.py is used to determine which value of mu to use in our experiments, as can be seen in the paper.



