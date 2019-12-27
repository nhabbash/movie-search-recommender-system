#script to hybrid raccomandation 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from keras.models import load_model
import random
import numpy as np
import ast

dataset = pd.read_csv("./data/dataset_rs.csv")
model = load_model('./data/model_cf.h5')
user_profile = pd.read_csv("./data/users_final.csv")

def metadata_user(userId):
    data = user_profile.query("user_id == "+str(userId))
    genres = data['genre_preferences'].values[0]
    genres = genres.split(",")
    if len(data['language'].values[0].split(",")) <= 1:
        language = data['language'].values[0]
    else :
        language = data['language'].values[0].split(",")
        language = "|".join(language).replace(" ", "")
    return {'lang': language, 'gen': "|".join(genres).replace(" ", "")}
	
def filter_metadata(X):
    data = dataset[dataset['genres'].str.contains(X['gen'], na = False)]
    data = data[data['spoken_languages'].str.contains(X['lang'], na = False)]
    return data[['movieId','title','overv_pp']] 

def map_user(user, tf):
    user = user[0]
    user_comp_bow = np.zeros(len(tf.get_feature_names()))
    indx = []
    for i in user[1]:
        if i in list(tf.get_feature_names()):
            n = list(tf.get_feature_names()).index(i)
            indx.append(n)
    cont=0
    for i in indx:
        user_comp_bow[i] = user[0][cont]
        cont+=1
    return user_comp_bow

def recommender_cb(user_metadata, user_bow, user_id):
    movies_user = filter_metadata(user_metadata)
    tf = TfidfVectorizer()
    tfidf_matrix = tf.fit_transform(movies_user['overv_pp'])
    cosine_similarities = linear_kernel(np.array([map_user(user_bow, tf)]), tfidf_matrix)[0]
    final_movies = []
    cs_sort = cosine_similarities.argsort()[::-1]
    cs_sort = list(set(movies_user.iloc[cs_sort,:]['movieId'].values))[0:10]
    for i in cs_sort:
        final_movies.append(movies_user.query("movieId == "+str(i)).head(1)['title'].values[0])
    return pd.DataFrame({'userId': [user_id]*10,'movieId':cs_sort, 'title':final_movies, 'type_r':['cb']*10})
	
def recommender_cf(user_id):
    movie_view = dataset.query("userId == "+ str(user_id))
    old_movie = movie_view['movieId'].values
    all_movie = list(set(dataset['movieId'].values))
    new_film = list(set(all_movie) - set(old_movie))
    random_film = random.sample(new_film, 50)
    pred=model.predict([[user_id]*50, np.array(random_film)])
    couple = list(zip(pred, random_film))
    top_couple = sorted(couple, key = lambda x : x[0])[-11:-1]
    top = [x[1] for x in top_couple][:: -1]
    final_movie =[]
    for i in top:
        final_movie.append(dataset.query("movieId == "+str(i))['title'].values[0])
    data = {'userId': [user_id]*10, 'movieId':top, 'title':final_movie, 'type_r':['cf']*10}  
    return pd.DataFrame(data)
    
 
list_users = list(user_profile['user_id'].values) 

metadata_u = metadata_user(list_users[0])
bow_u = ast.literal_eval(user_profile['bow'].values[0])
id_u = list_users[0]
df_cf = recommender_cf(id_u)
df_cb = recommender_cb(metadata_u,bow_u,id_u)
df = df_cf.append(df_cb)
for i in range(1,10):
    metadata_u = metadata_user(list_users[i])
    bow_u = ast.literal_eval(user_profile['bow'].values[i])
    id_u = list_users[i]
    b = recommender_cf(id_u)
    a = recommender_cb(metadata_u,bow_u,id_u)
    tmp = b.append(a)
    df = df.append(tmp)
	
df.to_csv('./data/user_recommender.csv', index = False)