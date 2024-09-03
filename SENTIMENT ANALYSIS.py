# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1I5L_nLEWPJ9FOeJyamjt625tW7VwmR8B
"""

import numpy as np
import pandas as pd

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

tweet_data = pd.read_csv('/content/Tweets.csv')
print("data shape:",tweet_data.shape)
print("what are columns:",tweet_data.columns)
tweet_data.head()

tweet_data = tweet_data.drop(['tweet_id','retweet_count', 'tweet_coord', 'tweet_created',
                               'tweet_location','name','user_timezone'],axis = 1)

tweet_data.head()

tweet_data['negativereason_gold'].unique()

tweet_data['negativereason'] = tweet_data['negativereason'].fillna('')
tweet_data['negativereason_confidence'] = tweet_data['negativereason_confidence'].fillna(0)
tweet_data['airline_sentiment_gold'] = tweet_data['airline_sentiment_gold'].fillna('')
tweet_data['negativereason_gold'] = tweet_data['negativereason_gold'].fillna('')

tweet_data.head()

print("different topics of negative reasons are:",tweet_data['negativereason'].unique())

!pip install contractions

from nltk.corpus import stopwords
import string
import re
import contractions
def text_cleaning(text):
    #not removing the stopwords so that the sentences stay normal.
    #forbidden_words = set(stopwords.words('english'))
    if text:
        text = contractions.fix(text)
        text = ' '.join(text.split('.'))
        text = re.sub(r'\s+', ' ', re.sub('[^A-Za-z0-9]', ' ', text.strip().lower())).strip()
        text = re.sub(r'\W+', ' ', text.strip().lower()).strip()
        text = [word for word in text.split()]
        return text
    return []

tweet_data['text'] = tweet_data['text'].apply(lambda x: ' '.join(text_cleaning(x)))

tweet_data.head(20)

import nltk

nltk.download(["names","stopwords","state_union","twitter_samples",
              "movie_reviews","averaged_perceptron_tagger","vader_lexicon",
              "punkt"])

from nltk.sentiment import SentimentIntensityAnalyzer as SIA
sia = SIA()
print(sia.polarity_scores('wow! this nltk library really works'))

texts = tweet_data['text'].tolist()
negative_scores = []
neutral_scores = []
positive_scores = []
compound_scores = []
final_tag = []
for text in texts:
    # Check if the text is a string before processing
    if isinstance(text, str):
        score_dictionary = sia.polarity_scores(text)
        negative_scores.append(score_dictionary['neg'])
        positive_scores.append(score_dictionary['pos'])
        neutral_scores.append(score_dictionary['neu'])
        compound_scores.append(score_dictionary['compound'])
        if score_dictionary['compound']>0:
            final_tag.append('positive')
        elif score_dictionary['compound']<0:
            final_tag.append('negative')
        else:
            final_tag.append('neutral')
    # Handle cases where text is not a string (e.g., float)
    else:
        negative_scores.append(None)  # Or any suitable default value
        positive_scores.append(None)
        neutral_scores.append(None)
        compound_scores.append(None)
        final_tag.append(None)
tweet_data['negative_score'] = negative_scores
tweet_data['positive_score'] = positive_scores
tweet_data['neutral_score'] = neutral_scores
tweet_data['compound_score'] = compound_scores
tweet_data['final_tag'] = final_tag

tweet_data.head(20)

texts[17]

# Check the data types of the relevant columns
print(tweet_data['airline_sentiment'].dtype)
print(tweet_data['final_tag'].dtype)

# Convert the columns to a consistent data type if necessary
# For example, to convert both columns to strings:
tweet_data['airline_sentiment'] = tweet_data['airline_sentiment'].astype(str)
tweet_data['final_tag'] = tweet_data['final_tag'].astype(str)

from sklearn.metrics import classification_report as crep
print("sentiment analysis performance for nltk:")
print(crep(tweet_data['airline_sentiment'],tweet_data['final_tag']))

!pip install -U textblob
!python -m textblob.download_corpora

from textblob import TextBlob

tb1 = TextBlob('I just am trying textblob first time.')
tb1

TextBlob("I just am trying textblob first time.")

tb1.words

tb1.sentences

tb1.noun_phrases

tb2=TextBlob("Tags will give the Part of speech for all the words.")
tb2.tags

tb3=TextBlob(" We are learning cool Library . We are enjoying a lot .")
tb3.noun_phrases

type(tb3.noun_phrases)

doc2=TextBlob("We are having fun here")
doc2.polarity

texts = tweet_data['text'].tolist()
textblob_score = []
textblob_tag = []
for text in texts:
    # Ensure score and tag are added for each text
    score = 0  # Default score if text is not a string
    tag = 'neutral'  # Default tag if text is not a string
    if isinstance(text, str):
        doc_current = TextBlob(text)
        score = doc_current.polarity
        if score > 0:
            tag = 'positive'
        elif score < 0:
            tag = 'negative'
    textblob_score.append(score)
    textblob_tag.append(tag)
tweet_data['textblob_score'] = textblob_score
tweet_data['textblob_sentiment_tag'] = textblob_tag

tweet_data[['airline_sentiment','text','textblob_score','textblob_sentiment_tag']].head(20)

print("sentiment analysis with textblob:")
print(crep(tweet_data['airline_sentiment'],tweet_data['textblob_sentiment_tag']))

from transformers import pipeline
classifier = pipeline('sentiment-analysis')
classifier("I am so happy to use huggingface today!")[0]['label']

classifier("it was a extremely bad movie!")[0]['label']

