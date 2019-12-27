#script to add bow at user 
import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer

dataset = pd.read_csv("./data/dataset_rs.csv")
users = pd.read_csv("./data/users.csv", delimiter = ";")

def create_bow_user(userId):
    data = dataset.query("userId == "+str(userId))[0:5]
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
    return user_bow, list(data['id'].values)
    

bow_list = []
film_list =[]
for i in users['user_id'].values:
    tmp = create_bow_user(i)
    bow_list.append(tmp[0:1])
    film_list.append(tmp[-1])

user_dic = {'films':film_list, 'bow':bow_list}
user_dataframe = pd.DataFrame(user_dic)
df = users.join(user_dataframe)
df.to_csv('./data/users_final.csv',index = False)
