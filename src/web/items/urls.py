from django.urls import path

from . import views

# app_name = 'items'
urlpatterns = [
    path('', views.search, name='search'),
    path('<int:film_id>/', views.info, name ="info")
]


