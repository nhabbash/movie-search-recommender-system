from django.urls import path

from . import views

app_name = 'items'
urlpatterns = [
    path('', views.SearchView.as_view(), name='search'),
    path('recommender/', views.RecommenderView.as_view(), name ='recommender')
]


