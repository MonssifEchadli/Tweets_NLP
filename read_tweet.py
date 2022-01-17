#!/usr/bin/env python
# coding: utf-8

# In[16]:


pip install findspark


# In[17]:


pip install pyspark


# In[18]:


import findspark
findspark.init()
import pyspark


# In[19]:


from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import desc


# In[20]:


sc = SparkContext()
ssc = StreamingContext(sc, 10)
sqlContext = SQLContext(sc)


# In[21]:


socket_stream = ssc.socketTextStream("127.0.0.1", 5555)
lines = socket_stream.window(60)


# In[22]:


from collections import namedtuple
fields = ("hashtag", "count" )
Tweet = namedtuple( 'Tweet', fields )
( lines.flatMap( lambda text: text.split( " " ) ) #Splits to a list
  # Checks for    hashtag calls  
  .filter( lambda word: word.lower().startswith("#") ) 
  .map( lambda word: ( word.lower(), 1 ) ) # Lower cases the word
  .reduceByKey( lambda a, b: a + b ) 
 # Stores in a Tweet Object
  .map( lambda rec: Tweet( rec[0], rec[1] ) )
 # Sorts Them in a dataframe
  .foreachRDD( lambda rdd: rdd.toDF().sort( desc("count") )
 # Registers only top 10 hashtags to a table.
  .limit(10).registerTempTable("tweets") ) )


# In[23]:


# start streaming and wait couple of minutes to get enought tweets
ssc.start()


# In[ ]:




