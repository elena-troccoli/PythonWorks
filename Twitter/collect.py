
# coding: utf-8

__author__ = 'mongolab'
MONGODB_URI = 'mongodb://adm2:admproject2@ds027495.mongolab.com:27495/adm' 

import tweepy
import pymongo
import time

client = pymongo.MongoClient(MONGODB_URI)

db = client.get_default_database()

followersDB2= db['followers2.0']
tweets = db['tweetBD']
users = db['users']

consumer_key = 'LJsdhVotaTs2d1rYixGKKzPGZ'
consumer_secret = 'toB43gqQZbar86HXsZC3s2IE9dpas8dYKXiINEjJoKRYR8wewn'
access_token = '4438940717-7F7TNmGUh4IA3lHG4SHOVqURBOIQDH7mme8UQpF'
access_token_secret = 'VrWggsUxEv4VxjOLBkTpp2eSFYKX828rxLU5PtI5EsLzg'
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
api = tweepy.API(auth)

#download 10'000 tweets
query='BigData'


for tweet in tweepy.Cursor(api.search, q=query, count=100).items():
            
    thisTweet = {}
    thisTweet["id"] = tweet.id
    thisTweet["userid"] = tweet.user.id
    thisTweet["text"] = tweet.text
    tweets.insert(thisTweet)


for i in range(100):
    maxid=tweets.find_one(sort=[("id", -1)])
    
    try:
        for tweet in tweepy.Cursor(api.search, q=query, count=100, max_id=maxid).items():
            thisTweet = {}
            thisTweet["id"] = tweet.id
            thisTweet["userid"] = tweet.user.id
            thisTweet["text"] = tweet.text
            tweets.insert(thisTweet)
                
    except tweepy.TweepError:
        # hit rate limit, sleep for 15 minutes
        print('Rate limited. Sleeping for 15 minutes.')
        time.sleep(15 * 60 + 15)
        continue



cursor = db.tweetBD.find()

#get all the users who tweeted
allUsers=[]
for tweet in cursor:
    userid=tweet['userid']
    if userid not in allUsers:
        allUsers.append(userid)

#create the collection of users
for user in allUsers:
    thisUser={}
    thisUser['userid'] = user
    users.insert(thisUser)


#for every user in the collection, i collect its followers 
#I store the information in the collection 'followers2.0'
cursor_follower = db.follower.find()
size = cursor_follower.count()

for user in db.users.find(no_cursor_timeout=True):
    thisUserid=user["userid"]
    ids = []
    
    try:
        for page in tweepy.Cursor(api.followers_ids, user_id=thisUserid).pages():
            ids.extend(page)
        
    except tweepy.TweepError:
        # hit rate limit, sleep for 15 minutes
        print('Rate limited. Sleeping for 15 minutes.')
        time.sleep(15 * 60 + 15)
        continue
    followersDB2.insert_one({'userid': thisUserid, 'followers': ids})    

client.close()

