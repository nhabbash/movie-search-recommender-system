#script per il preprocessing overviews
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from ast import literal_eval
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer 
import numpy as np

dataset = pd.read_csv("./data/parsed_dataset.csv", delimiter = ";")
ratings = pd.read_csv("./data/ratings_small.csv")

#preprocessing overwies
stop_words = set(stopwords.words('english'))
def stop_word(x):
    word_tokens = word_tokenize(x)
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    return filtered_sentence

def remove_punctuation(data):
    symbols = "!\"#$%&()*+-,\/./:;<=>?@[\]^_`{|}~\n-"
    for i in symbols:
        data = np.char.replace(data, i, '')
    data = np.char.replace(data, "'", "")
    tmp =[]
    for i in data:
        if len(i) > 1:
            tmp.append(i)
    return tmp

def stemming(data):
    ps = PorterStemmer() 
    tmp=[]
    for w in data:
        tmp.append(ps.stem(w))
    return tmp

corpus =[]

for i in list(dataset['overview'].values):
    i = np.char.lower(i)
    i = stop_word(str(i))
    i = stemming(i)
    if i != []:
        i = remove_punctuation(i)
    corpus.append(' '.join(i))

dataset['overv_pp'] = corpus
dataset = dataset[['id','title','overv_pp','genres','spoken_languages','original_language']]

complete_data = dataset.join(ratings.set_index('movieId'), on= 'id')
complete_data = complete_data[np.isfinite(complete_data['rating'])]

item_enc = LabelEncoder()
complete_data['movieId'] = item_enc.fit_transform(complete_data['id'].values)

complete_data.to_csv('./data/dataset_rs.csv', index= False)