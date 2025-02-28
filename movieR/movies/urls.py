from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/create/', views.movie_create, name='movie_create'),
    path('movie/<int:movie_id>/update/', views.movie_update, name='movie_update'),
    path('movie/<int:movie_id>/delete/', views.movie_delete, name='movie_delete'),
    path('movie/<int:movie_id>/review/', views.review_create, name='review_create'),
]