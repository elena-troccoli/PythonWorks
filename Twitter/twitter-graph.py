
# coding: utf-8

import csv
import pandas as pd
import networkx as nx
import numpy as np


#I retireve my twitter graph from the csv file
twitter = pd.read_csv('edgesTwitter.csv', delimiter=',', comment='#', header=None)
l=[(twitter.iloc[i,0], twitter.iloc[i,1]) for i in range(len(twitter))]
G=nx.DiGraph()
G.add_edges_from(l)

degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence

#print "Degree sequence", degree_sequence
#dmax=max(degree_sequence)

plt.loglog(degree_sequence, 'b-', marker='o')
plt.title("Degree rank plot")
plt.ylabel("degree")
plt.xlabel("rank")
plt.savefig("degree_histogram_twitter.png")
plt.show()

#compute centrality, betweenness, closeness and pagerank. 
#Store the info into a csv file
centrality=nx.degree_centrality(G)

between=nx.betweenness_centrality(G)

close=nx.closeness_centrality(G)

pagerank=nx.pagerank(G)

f = open('output.csv', 'wt')
try:
    writer = csv.writer(f)
    writer.writerow( ('node', 'centrality', 'betweenness', 'closeness', 'pagerank') )
    for n  in centrality.keys():
        writer.writerow((n,centrality[n] ,between[n], close[n], pagerank[n] ))
finally:
    f.close()

#convert G into an undirected graph in order to compute clustering coefficients
#Store the info into a csv file
undirG = G.to_undirected()
average_clustering=nx.average_clustering(undirG)
clustering_coefficient = nx.clustering(undirG)
f = open('clustering.csv', 'wt')
try:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow((('Average Clustering Coefficient of the Graph: ', average_clustering ) ))
    
    writer.writerow( ('Node','Clustering Coefficient') )
    for n, c  in clustering_coefficient.iteritems():
        writer.writerow((n , c))
finally:
    f.close()

#Compute the connected components in the directed copy of the graph G
connected_components = [c for c in sorted(nx.connected_components(undirG), key=len, reverse=True)]

#Compute the strongly connected components in the directed graph G
strong_connected_components = [c for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]

#write the information into a csv file
f = open('conn-comp-twitter.csv', 'wt')
try:
    writer = csv.writer(f, delimiter='\t')
    
    writer.writerow(('There are' , len(connected_components), 'connected components in the undirected copy of the twitter graph' ))
    len_conn = [len(c) for c in connected_components]
    number={k: len_conn.count(k) for k in len_conn }
    for cardinality, number  in number.iteritems():
        writer.writerow((number, 'connected components with  ', cardinality, 'nodes'))
    
    
    writer.writerow(('There are' , len(strong_connected_components), 'strongly connected components in the directed twitter graph' ))
    len_strongly = [len(c) for c in strong_connected_components]
    number={k: len_strongly.count(k) for k in len_strongly }
    for cardinality, number  in number.iteritems():
        writer.writerow((number, 'strongly connected components with  ', cardinality, 'nodes'))
finally:
    f.close()

largest_component=G.subgraph(connected_components[0]) 

#compute the k-core decomposition of the largest component


k_cores=[]
hcore=n=nx.k_core(G, k=0)
h=1
while len(hcore)!=0:
    hcore=nx.k_core(largest_component, k = h)
    k_cores.append(hcore)
    h+=1

len_core = [len(c) for c in k_cores]

#save the information about the k-core decomposition into a csv file
f = open('k-cores-twitter.csv', 'wt')
try:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(('k core decomposition for the largest connected component',))
    
    len_core = [len(c) for c in k_cores]
    
    for k, cardinality in enumerate(len_core):
        writer.writerow(('k =', k , 'number of nodes: ', cardinality))
    
finally:
    f.close()

#plot k-core decomposition
y =sorted(len_core,reverse=False) 

plt.plot(y, 'b-', marker='o')
plt.title("K-cores plot")
plt.ylabel("cardinality of the k-core")
plt.xlabel("k")
plt.axis([-100, max(x)+100, -100, max(y)+100])
plt.savefig("k-cores-twitter.png")


