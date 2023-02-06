# -*- coding: utf-8 -*-
"""Copy of Sentiment Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/129aBzIq5dMkeEGSMOTfg2r8CPWXULSTW
"""

# Import the necessary packages
from wordcloud import WordCloud # for visualizing word frequency
from textblob import TextBlob # for sentiment analysis
from textblob.sentiments import NaiveBayesAnalyzer # for sentiment analysis with Naive Bayes
import matplotlib.pyplot as plt # for plotting
import plotly.express as px # for plotting
import pandas as pd # for data manipulation and analysis
import numpy as np # for numerical computations
import tweepy # for accessing the Twitter API
import re # for text cleaning
import nltk # for NLP tasks

# set a style for plots
plt.style.use('fivethirtyeight')

# Read the Twitter API credentials from a csv file
credentials = pd.read_csv('credentials.csv')

# Create the authentication object to access the API
authenticate = tweepy.OAuthHandler(credentials['consumerKey'][0], credentials['consumerSecret'][0])

# Set the access token and access token secret for API access
authenticate.set_access_token(credentials['accessToken'][0],credentials['accessTokenSecret'][0])

# Create the API object with the authentication details
api=tweepy.API(authenticate, wait_on_rate_limit=True)

# Search for tweets with a specific term and store the returned tweets
search_term="spx -filter:retweets"
tweets=tweepy.Cursor(api.search,q=search_term,lang='en',since='2021-11-01',tweet_mode='extended').items(100)
posts=[tweet.full_text for tweet in tweets]

# Store the extracted tweets in a dataframe
df=pd.DataFrame(posts, columns=["Tweets"])

#Create a function to clean text 
def cleanText(text):
  # text=re.sub('#',' ',text) #Remove hashtags
  text=re.sub('@\S+',' ',text) #Remove mentions
  text=re.sub( 'https?:\/\/\S+',' ',text) #Remove hyperlinks
  text=re.sub('\\n',' ',text) #Remove Retweets
  return text

# Apply the cleanText function on all tweets
df['Tweets']=df['Tweets'].apply(cleanText)

#Create a function the subjectivity 
def getSubjectivitty(text):
  return TextBlob(text).sentiment.subjectivity

#create a function to get polarity
def getPolarity(text):
  return TextBlob(text).sentiment.polarity

# Apply the getSubjectivity and getPolarity functions to the 'Tweets' column of the DataFrame
df['subjectivity'] = df['Tweets'].apply(getSubjectivity)

# Calculate the polarity of each tweet and store it in a new 'polarity' column
df['polarity'] = df['Tweets'].apply(getPolarity)

# Show the first five rows of the dataframe with the added columns
df.head()

#Visualize wordcloud
allwords=' '.join([twts for twts in df['Tweets']])
wordCloud = WordCloud(width=800, height=450, random_state=1, max_font_size=100).generate(allwords)
plt.imshow(wordCloud)
plt.axis('off')

# Define a function to get the analysis based on the polarity score
def getAnalysis(score):
    if score < 0:
      return 'Negative'
    elif score == 0:
      return 'Neutral'
    else:
      return 'Positive'

# Add the analysis column to the dataframe
df['Analysis']=df['polarity'].apply(getAnalysis)

# Print all positive tweets, sorted by most positive first
j = 1
sortedDF = df.sort_values(by=['polarity'])
for i in range(0, sortedDF.shape[0]):
  if(sortedDF['Analysis'][i] == 'Positive'):
    print(str(j) + ')' + sortedDF['Tweets'][i] + '\n')
    j += 1

# Print all negative tweets, sorted by most negative first
j=1
sortedDF=df.sort_values(by=['polarity'])
for i in range(0, sortedDF.shape[0]):
  if(sortedDF['Analysis'][i]=='Negative'):
    print(str(j)+')'+ sortedDF['Tweets'][i]+'\n')
    j+=1

# #Get the percentage of each category of tweets
positive=(df.query("Analysis=='Positive'")['Tweets'].count()/df['Tweets'].count())
print("% of positive tweets",positive)
negative=(df.query("Analysis=='Negative'")['Tweets'].count()/df['Tweets'].count())
print("% of negative tweets",negative)
Neutral=(df.query("Analysis=='Neutral'")['Tweets'].count()/df['Tweets'].count())
print("% of negative tweets",Neutral)

#Plot the polarity and subjectivity 
plt.figure(figsize=(8,6))
for i in range(0,df.shape[0]):
  plt.scatter(df['polarity'][i],df['subjectivity'][i],color="blue")
plt.title("Sentiment analysis")
plt.xlabel("Polarity")
plt.ylabel("Subjectivty")

# Plot the count of each sentiment analysis
df['Analysis'].value_counts()
plt.title("Sentiment Analysis")
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind='bar')
plt.show()