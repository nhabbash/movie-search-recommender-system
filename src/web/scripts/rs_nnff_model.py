#neural network to matrix factorization
import pandas as pd
dataset = pd.read_csv('ratings_small.csv')

## import libraries
%matplotlib inline

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import keras
from keras import backend as K
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
## import keras models, layers and optimizers
from sklearn.metrics import mean_absolute_error, mean_squared_error
from keras.models import Sequential, Model
from keras.layers import Embedding, Flatten, Dense, Dropout, concatenate, multiply, Input
from keras.optimizers import Adam
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import KFold
from keras.callbacks import EarlyStopping
#dataset = pd.read_csv("./books/ratings.csv")

n_users, n_books = len(dataset.userId.unique()), len(dataset.movieId.unique())

#codifica degli utenti e risorse per evitare i salti tra IDs
user_enc = LabelEncoder()
dataset['user'] = user_enc.fit_transform(dataset['userId'].values)
n_users = dataset['user'].nunique()

item_enc = LabelEncoder()
dataset['movie'] = item_enc.fit_transform(dataset['movieId'].values)
n_movies = dataset['movie'].nunique()

dataset['rating'] = dataset['rating'].values.astype(np.float32)
min_rating = min(dataset['rating'])
max_rating = max(dataset['rating'])
n_users, n_movies, min_rating, max_rating

#split in train e test set 
X = dataset[['user', 'movie']].values
y = dataset['rating'].values
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=0)

#normalizzazione 
n_ratings = len(set(list(y_train)))

y_train = y_train / n_ratings
y_test = y_test / n_ratings

#iper parametri neural network
embedding_size = 100
dim_first = 100
dim_second = 50
epochs_n = 50
batch_n = 512
seed = 7
np.random.seed(seed)
kf = KFold(n_splits=10, random_state = seed, shuffle = True)

#definizione del modello 
user_input = Input(shape=[1], name='user')
item_input = Input(shape=[1], name='item')

embedding_u = keras.layers.Embedding(n_users , embedding_size, name='Embedding_user')(user_input)
embedding_b = keras.layers.Embedding(n_movies , embedding_size, name='Embedding_movie')(item_input)

flatten_u = Flatten(name='Flatten_user')(embedding_u)
flatten_b = Flatten(name='Flatten_movie')(embedding_b)
user_vecs = Dense(dim_first, activation='relu')(flatten_u) 
item_vecs = Dense(dim_first, activation='relu')(flatten_b)

input_vecs = concatenate([user_vecs, item_vecs],name='Concat')

x = Dense(dim_first, activation='relu')(input_vecs)
x = Dense(dim_second, activation='relu')(x)
y = full_c = Dense(1, activation = 'sigmoid')(x)

es = EarlyStopping(monitor='val_mean_squared_error', mode='min', verbose=1, patience=5)
model = Model(inputs=[user_input, item_input], outputs=y)
adam = keras.optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.99, amsgrad=False)
model.compile(loss='mse', optimizer=adam, metrics=['mse'])

X = x_train
Y = y_train
cvscores = []
history_list = []

#training step
for train, test in kf.split(X):
  history_list.append(model.fit([X[train][:,0], X[train][:,1]], Y[train], epochs=epochs_n, batch_size=batch_n ,verbose=1, validation_split=0.1, shuffle=True,callbacks=[es]))
  scores = model.evaluate([X[test][:,0],X[test][:,1]], Y[test])
  print(model.metrics_names[1], scores[1])
  cvscores.append(scores[1])
  
print("errore medio della fase 10 cross fold validation")
print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))

#test step
pred=model.predict([x_test[:,0], x_test[:,1]])
prediction = pred
print("errore per la fase di test")
print(mean_squared_error(y_test, prediction))

#save model
model.save("model_cf.h5")
model.save_weights("model_cf__weights.h5")