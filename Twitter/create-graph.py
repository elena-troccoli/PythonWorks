# coding: utf-8

__author__ = 'mongolab'
MONGODB_URI = 'mongodb://adm2:admproject2@ds027495.mongolab.com:27495/adm'

import pymongo
import csv
import networkx as nx

client = pymongo.MongoClient(MONGODB_URI)

db = client.get_default_database()

users = db['users']
followersDB2= db['followers2.0']

cursor_followers = db.followersDB2.find()
cursor_users = db.users.find()


#get the list of all the users from my mongoDB MongoLab
allUsers=[]
for user in cursor_users:
    userid=user['userid']
    if userid not in allUsers:
        allUsers.append(userid)


followersDB2= db['followers2.0']
for user in followersDB2.find(no_cursor_timeout=True):
    thisUser=user['userid']
    followers=user['followers']
    BDfollower=[follower for follower in followers if follower in allUsers]
    l=[(thisUser, follower) for follower in BDfollower]
    G.add_edges_from(l)

#I save G into a csv file
#The file is 'edgesTwitter.csv'
#
edges=nx.edges(G)
f = open('edgesTwitter.csv', 'wt')
try:
    writer = csv.writer(f)
    writer.writerow( ('#from', 'to') )
    for edge  in edges:
        writer.writerow((edge[0], edge[1]))
finally:
    f.close()
	
client.close()