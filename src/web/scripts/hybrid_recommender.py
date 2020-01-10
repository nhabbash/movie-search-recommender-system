#script to hybrid raccomandation 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from keras.models import load_model
import random
import numpy as np
import ast
from ast import literal_eval

dataset = pd.read_csv("../data/dataset_rs.csv")
model = load_model('../data/model_cf.h5')
user_profile = pd.read_csv("../data/users_final.csv")
parsed_dataset = pd.read_csv("../data/parsed_dataset.csv", delimiter = ";")

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
	
def map_value(x):
    values = []
    for i in x:
        if i <= 0.05:
            values.append(0.5)
        elif i <= 0.1:
            values.append(1)
        elif i <= 0.15:
            values.append(1.5)
        elif i <= 0.2:
            values.append(2)
        elif i <= 0.25:
            values.append(2.5)
        elif i <= 0.3:
            values.append(3)
        elif i <= 0.35:
            values.append(3.5)
        elif i <= 0.4:
            values.append(4)
        elif i <= 0.45:
            values.append(4.5)
        else:
            values.append(5)
    return values

def filter_metadata(X, all_data = False):
    data = dataset[dataset['genres'].str.contains(X['gen'], na = False)]
    data = data[data['spoken_languages'].str.contains(X['lang'], na = False)]
    if all_data :
        data = data.drop_duplicates(subset='id', keep="last")
        return data

    data = data[['id','title','overv_pp']] 
    data = data.drop_duplicates(subset='id', keep="last")
    return data

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

def filter_metadata_cb(X, all_filter = False):
    if all_filter:
        data = parsed_dataset[parsed_dataset['genres'].str.contains(X['gen'], na = False)]
        data = data[data['spoken_languages'].str.contains(X['lang'], na = False)]
    else :
        data = parsed_dataset[parsed_dataset['spoken_languages'].str.contains(X['lang'], na = False)]
    data = data[['id','title','overv_pp']] 
    data = data.drop_duplicates(subset='id', keep="last")
    return data

def recommender_cb(user_metadata, user_bow, user_id, filtering = False):
    if not(filtering) :
        movies_user = filter_metadata_cb(user_metadata)
    else :
        movies_user = filter_metadata_cb(user_metadata, True)
    tf = TfidfVectorizer()
    movies_user = movies_user.dropna(axis=0, subset=['overv_pp'])
    tfidf_matrix = tf.fit_transform(movies_user['overv_pp'])
    cosine_similarities = linear_kernel(np.array([map_user(user_bow, tf)]), tfidf_matrix)[0]
    cs_sort = cosine_similarities.argsort()[::-1]
    history_films = literal_eval(user_profile.query("user_id == "+str(user_id))['film_ratings'].values[0])
    history_films = [i[0] for i in history_films]
    id_films = []
    rank = []
    for i in cs_sort:
        if not(movies_user['id'].values[i] in history_films):
            id_films.append(movies_user['id'].values[i])
            rank.append(cosine_similarities[i])
        if len(id_films) == 10 :
            break
    final_movies = []
    for i in id_films:
        final_movies.append(movies_user.query("id == "+str(i)).head(1)['title'].values[0])
    return pd.DataFrame({'userId': [user_id]*10,'movieId':id_films, 'title':final_movies, 'type_r':['cb']*10,'rank':rank})
	
	
def recommender_cf(user_id, filter_md = False):
    if filter_md :
        mu = filter_metadata(metadata_user(user_id), True)
        movies_user = mu.drop_duplicates(subset='id', keep="last")
        movies_user = movies_user.query("userId == "+ str(user_id))
        old_movie = movies_user['movieId'].values
        all_movie = list(set(mu['movieId'].values))
        new_film = list(set(all_movie) - set(old_movie))      
        temp_id = int(mu.query('userId == '+str(user_id))['user_id'].values[0])
        pred=model.predict([[temp_id]*len(new_film), np.array(new_film)])
        couple = list(zip(pred, new_film))
        top_couple = sorted(couple, key = lambda x : x[0])
        top_movieId = [x[1] for x in top_couple][:: -1]
        top_rate = map_value([x[0] for x in top_couple][:: -1])
        title_movie = []
        id_movie = []
        for i in top_movieId:
            title_movie.append(dataset.query("movieId == "+str(i))['title'].values[0])
            id_movie.append(dataset.query("movieId == "+str(i))['id'].values[0])
        data = {'userId': [user_id]*len(id_movie), 'movieId':id_movie, 'title':title_movie, 'type_r':['cf']*len(id_movie),'rank':top_rate}
        return pd.DataFrame(data)[0:10]
    
    movie_view = dataset.query("userId == "+ str(user_id))
    old_movie = movie_view['movieId'].values
    all_movie = list(set(dataset['movieId'].values))
    new_film = list(set(all_movie) - set(old_movie))
    random_film = random.sample(new_film, 50)
    temp_id = int(dataset.query('userId == '+str(user_id))['user_id'].values[0])
    pred=model.predict([[temp_id]*len(new_film), np.array(new_film)])
    couple = list(zip(pred, new_film))
    top_couple = sorted(couple, key = lambda x : x[0])[-11:-1]
    top_movieId = [x[1] for x in top_couple][:: -1]
    top_rate = map_value([x[0] for x in top_couple][:: -1])
    title_movie = []
    id_movie = []
    for i in top_movieId:
        title_movie.append(dataset.query("movieId == "+str(i))['title'].values[0])
        id_movie.append(dataset.query("movieId == "+str(i))['id'].values[0])
    data = {'userId': [user_id]*10, 'movieId':id_movie, 'title':title_movie, 'type_r':['cf']*10,'rank':top_rate}  
    return pd.DataFrame(data)
    

def recommender_step(filtering = False):
	list_users = list(user_profile['user_id'].values)
	metadata_u = metadata_user(list_users[0])
	bow_u = ast.literal_eval(user_profile['bow'].values[0])
	id_u = list_users[0]
	df_cf = recommender_cf(id_u, filtering)
	df_cb = recommender_cb(metadata_u,bow_u,id_u, filtering)
	df = df_cf.append(df_cb)

	if len(list_users) > 1:
		for i in range(1,len(list_users)):
			metadata_u = metadata_user(list_users[i])
			bow_u = ast.literal_eval(user_profile['bow'].values[i])
			id_u = list_users[i]
			b = recommender_cf(id_u, filtering)
			a = recommender_cb(metadata_u,bow_u,id_u, filtering)
			tmp = b.append(a)
			df = df.append(tmp)
	return df[df['rank'] > 0 ]

recommender_step().to_csv('../data/user_recommender.csv', index = False)
recommender_step(True).to_csv('../data/user_recommender_filter.csv', index = False)

