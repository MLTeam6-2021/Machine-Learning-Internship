import pandas as pd

train = pd.read_csv('TAPAS_SCRAPED_DATA_20210731113158.csv')

# print(train.head())

train['word_count'] = train['Topic Title'].apply(lambda x: len(str(x).split(" ")))
# print(train[['Topic Title','word_count']].head())

train['char_count'] = train['Topic Title'].str.len() ## this also includes spaces
# print(train[['Topic Title','char_count']].head())

def avg_word(sentence):
    words = sentence.split()
    return (sum(len(word) for word in words)/len(words))

train['avg_word'] = train['Topic Title'].apply(lambda x: avg_word(x))
# print(train[['Topic Title','avg_word']].head())


from nltk.corpus import stopwords

stop = stopwords.words('english')
# print(stop[:10])

train['stopwords'] = train['Topic Title'].apply(lambda x: len([x for x in x.split() if x in stop]))
# print(train[['Topic Title','stopwords']].head())

train['hastags'] = train['Topic Title'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))
# print(train[['Topic Title','hastags']].head())

train['hastags'] = train['Topic Title'].apply(lambda x: len([x for x in x.split() if x.startswith('@')]))
# print(train[['Topic Title','hastags']].head())

train['numerics'] = train['Topic Title'].apply(lambda x: len([x for x in x.split() if x.isdigit()]))
# print(train[['Topic Title','numerics']].head())

dummy_data = 'I have bought 50 books'
nbr_of_numerics = lambda x: len([x for x in x.split() if x.isdigit()])

# print(nbr_of_numerics(dummy_data))

train['upper'] = train['Topic Title'].apply(lambda x: len([x for x in x.split() if x.isupper()]))
# print(train[['Topic Title','upper']].head())

train['Topic Title'] = train['Topic Title'].apply(lambda x: " ".join(x.lower() for x in x.split()))
# print(train['Topic Title'].head())

train['Topic Title'] = train['Topic Title'].str.replace('[^\w\s]','')
# print(train['Topic Title'].head())

train['Topic Title'] = train['Topic Title'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
# print(train['Topic Title'].head())

freq = pd.Series(' '.join(train['Topic Title']).split()).value_counts()[:10]
# print(freq)

train_data = train.copy()

freq = list(freq.index)
train['Topic Title'] = train['Topic Title'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
# print(train['Topic Title'].head())

freq = pd.Series(' '.join(train['Topic Title']).split()).value_counts()[-10:]
# print(freq)

freq = list(freq.index)
train['Topic Title'] = train['Topic Title'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
# print(train['Topic Title'].head())

from textblob import TextBlob

# print(train['Topic Title'][:5].apply(lambda x: str(TextBlob(x).correct())))

import nltk
nltk.download('punkt')

# print(TextBlob(train['Topic Title'][0]).words)

from nltk.stem import PorterStemmer

st = PorterStemmer()
# print(train['Topic Title'][:5].apply(lambda x: " ".join([st.stem(word) for word in x.split()])))

nltk.download('wordnet')

from textblob import Word

train['Topic Title'] = train['Topic Title'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
# print(train['Topic Title'].head())

# print(TextBlob(train['Topic Title'][0]).ngrams(2))

tf1 = (train['Topic Title'][0:3]).apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0).reset_index()
tf1.columns = ['words','tf']
# print(tf1)

import numpy as np

for i,word in enumerate(tf1['words']):
      tf1.loc[i, 'idf'] = np.log(train.shape[0]/(len(train[train['Topic Title'].str.contains(word)])))
# print(tf1)

tf1['tfidf'] = tf1['tf'] * tf1['idf']
# print(tf1)

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=1000, lowercase=True, analyzer='word',
 stop_words= 'english',ngram_range=(1,1))
train_vect = tfidf.fit_transform(train['Topic Title'])
# print(train_vect)
# print(train_data.head())

tfidf = TfidfVectorizer(max_features=1000, lowercase=True, analyzer='word',
 stop_words= 'english',ngram_range=(1,1))
train_vect2 = tfidf.fit_transform(train_data['Topic Title'])
# print(train_vect2)

tf2 = (train_data['Topic Title'][0:3]).apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0).reset_index()
tf2.columns = ['words','tf']
# print(tf2)


for i,word in enumerate(tf2['words']):
      tf2.loc[i, 'idf'] = np.log(train_data.shape[0]/(len(train_data[train_data['Topic Title'].str.contains(word)])))
# print(tf2)

tf2['tfidf'] = tf2['tf'] * tf2['idf']
compare = pd.DataFrame({"words": tf1["words"],
                        "tf1_result": tf1['tfidf'],
                        "tf2_result": tf2['tfidf']})
# print(compare)

# print(train_data.isna().sum())

# print(train.isna().sum())

from sklearn.feature_extraction.text import CountVectorizer

bow = CountVectorizer(max_features=1000, lowercase=True, ngram_range=(1,1),analyzer = "word")
train_bow = bow.fit_transform(train['Topic Title'])
# print(train_bow)

# print(train['Topic Title'][:5].apply(lambda x: TextBlob(x).sentiment))

train['sentiment'] = train['Topic Title'].apply(lambda x: TextBlob(x).sentiment[0] )
# print(train[['Topic Title','sentiment']].head())

corpus=[]
new= train['Topic Title'].str.split()
new=new.values.tolist()
corpus=[word for i in new for word in i]

from collections import defaultdict
dic=defaultdict(int)
for word in corpus:
    if word in stop:
        dic[word]+=1

def get_top_ngram(corpus, n=None):
    vec = CountVectorizer(ngram_range=(n, n)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) 
                  for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:10]



import seaborn as sns
import matplotlib.pyplot as plt

top_n_bigrams=get_top_ngram(train['Topic Title'],2)[:10]
x,y=map(list,zip(*top_n_bigrams))
sns.barplot(x=y,y=x)
plt.show()

top_tri_grams=get_top_ngram(train['Topic Title'],n=3)
x,y=map(list,zip(*top_tri_grams))
plt.show()

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS)

def show_wordcloud(data):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=100,
        max_font_size=30,
        scale=3,
        random_state=1)
   
    wordcloud=wordcloud.generate(str(data))

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')

    plt.imshow(wordcloud)
    plt.show()

show_wordcloud(corpus)