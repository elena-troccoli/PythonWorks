Twitter

The aim of these scripts is to download Twitter data using the tweepy library to access its API. 
We then store the results into MongoDB and perform some metrics computation on the retrieved graphs.

1. collect.py that collects more than 10000 tweets using the query 'BigData' and stores all the
information (tweet, user who tweeted and his/her followers) into a MongoDB in MongoLab.

2. create-graph.py : connects with the db on MongoLab and create the graph of the users who
wrote the tweets I previously downloaded.The graph that this script creates is a directed graph.
This script also stores the graph into a csv file named edgesTwitter.csv .

3. The script twitter-graph.py performs some computation over the graph (betweenness centrality, closeness centrality, page rank...), saving the results into different csv files.