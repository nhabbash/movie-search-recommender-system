#script per il preprocessing overviews
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from ast import literal_eval
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer 
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re

dataset = pd.read_csv("../data/parsed_dataset.csv", delimiter = ";")
ratings = pd.read_csv("../data/ratings_small.csv")
users = pd.read_csv("../data/users.csv")

# Insert user history in ratings_small
def add_user_custom_ratings():
    for index, row in users.iterrows():
        film_ratings = re.findall('\(\W*([\w\s]*?)\W*,\W*([\w\s]*?)\W*\)', row["film_ratings"])

    for film in film_ratings:
        global ratings
        ratings = ratings.append({"userId": row["user_id"],
                        "movieId": film[0],
                        "rating": film[1]}, ignore_index=True)
    
    ratings.to_csv('../data/ratings_small_extended.csv',index= False)

add_user_custom_ratings()

ratings = pd.read_csv("../data/ratings_small_extended.csv")

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

complete_data.to_csv('../data/dataset_rs.csv', index= False)

#create user final , add bow and history_films with ratings
def create_bow_user(userId):
    ids = users.query("user_id == "+str(userId))['film_ratings'].values[0]
    ids = literal_eval(ids)
    ids = [i[0] for i in ids]
    data = complete_data[complete_data['id'].isin(ids)]
    data = data.drop_duplicates(subset='id', keep="last")
    tf_u = TfidfVectorizer()
    tfidf_matrix_u = tf_u.fit_transform(data['overv_pp'])
    user_bow = [tfidf_matrix_u.toarray()[0], tf_u.get_feature_names()]
    weight=[]
    term=[]
    for i in range(len(user_bow[0])):
        if user_bow[0][i] != 0:
            weight.append(user_bow[0][i])
            term.append(user_bow[1][i])
    
    user_bow = [weight,term]
    return user_bow, list(data['id'].values), list(data['rating'].values)
    
bow_list = []
film_list =[]
for i in users['user_id'].values:
    tmp = create_bow_user(i)
    bow_list.append(tmp[0:1])
    film_list.append(list(zip(tmp[1],tmp[2])))
user_dic = {'bow':bow_list}

user_dataframe = pd.DataFrame(user_dic)

df = users.join(user_dataframe)

df.to_csv('../data/users_final.csv',index = False)
