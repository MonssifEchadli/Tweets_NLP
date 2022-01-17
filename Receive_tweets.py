#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy
from tweepy.auth import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json


# In[11]:


import pandas as pd
import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt


# In[2]:


consumer_key = 'w3sVgFkzNrDFzVGhQqWq4Relc'
consumer_secret = '33b9sHlnViMdmWMkFyISmq6e5QuvBs0XOg8XtwElLqgI08zO5M'
access_token = '1482395906355965958-MGXgL3tggoKscfrBVEkWeyvL0qkj72'
access_secret = 'tsP59AegCRQnMgJpG47GwZnpzcDnCzIRN0Hj64PWnkUXl'


# In[3]:


# we create this class that inherits from the StreamListener in tweepy StreamListener
class TweetsListener(StreamListener):

    def __init__(self, csocket):
        self.client_socket = csocket
    # we override the on_data() function in StreamListener
    def on_data(self, data):
        try:
            message = json.loads( data )
            print( message['text'].encode('utf-8') )
            self.client_socket.send( message['text'].encode('utf-8') )
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def if_error(self, status):
        print(status)
        return True


# In[4]:


def send_tweets(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=['Covid']) #we are interested in this topi


# In[5]:


if __name__ == "__main__":
    new_skt = socket.socket()         # initiate a socket object
    host = "127.0.0.1"     # local machine address
    port = 5555                 # specific port for your service.
    new_skt.bind((host, port))        # Binding host and port

    print("Now listening on port: %s" % str(port))

    new_skt.listen(5)                 #  waiting for client connection.
    c, addr = new_skt.accept()        # Establish connection with client. it returns first a socket object,c, and the address bound to the socket

    print("Received request from: " + str(addr))
    # and after accepting the connection, we aill sent the tweets through the socket
    send_tweets(c)


# In[8]:


authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret)
authenticate.set_access_token(access_token,access_secret)

api = tweepy.API(authenticate, wait_on_rate_limit = True)


# In[9]:


posts = api.search(q='#covid', count=500, lang="en", tweet_mode="extended")
for tweet in posts[0:99]:
  print(tweet.full_text + '\n')


# In[12]:


df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
df.head()


# In[13]:


def cleanTxt(text):
  text = re.sub(r'@[A-Za-z0-9]+','',text)
  text = re.sub(r'#','',text)
  text = re.sub(r'RT[\s]+','',text)
  text = re.sub(r'http?s:\/\/\S+','',text)#Remove hyper link
  return text
df ['Tweets'] = df ['Tweets'].apply(cleanTxt)
df


# In[14]:


def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
  return TextBlob(text).sentiment.polarity


# In[16]:


df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)
df

allWords =' '.join([twts for twts in df['Tweets']])

plt.axis('off')


# In[17]:


def getAnalysis(score):
  if score<0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'


df['Analysis'] = df['Polarity'].apply(getAnalysis)

df


# In[18]:


sortedDF = df.sort_values(by=['Polarity'])

for i in range(0,sortedDF.shape[0]):
  if(sortedDF['Analysis'][i] == 'Positive'):
    print(sortedDF['Tweets'][i])
    print()


# In[26]:


plt.figure(figsize=(8,6))
for i in range(0,df.shape[0]):
  plt.scatter(df['Polarity'][i], df['Subjectivity'][i],color='red' )

plt.title('Analyse de sentiments de COVID')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')

plt.show()

ptweets = df[df.Analysis == 'Positive']
ptweets = ptweets['Tweets']

round( (ptweets.shape[0] / df.shape[0])*100, 1)

df['Analysis'].value_counts()

plt.title('Sentiment Analysis for covid')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind='barh', color='red')
plt.style.use('fivethirtyeight')
plt.show()


# In[ ]:




