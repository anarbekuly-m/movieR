from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (
    MovieListView, MovieDetailView, MovieCreateView,
    MovieUpdateView, MovieDeleteView,
    review_create, upload_poster
)

from rest_framework.routers import DefaultRouter

from .api_view import (
    MovieListCreateAPIView,
    MovieRetrieveUpdateDestroyAPIView,
    CategoryListCreateAPIView,
    ReviewListCreateAPIView,
    WatchlistRetrieveAPIView,
    WatchlistAddMovieAPIView,
    WatchlistRemoveMovieAPIView
)

urlpatterns = [
    path('silk/', include('silk.urls', namespace='silk')),
    path('movies/', MovieListCreateAPIView.as_view(), name='movie-list-create'),
    # GET for listing and POST for creating
    path('movies/get/', MovieListCreateAPIView.as_view(), name='movie-list'),  # GET for listing
    path('movies/post/', MovieListCreateAPIView.as_view(), name='movie-create'),  # POST for creating
    path('movies/<int:pk>/', MovieRetrieveUpdateDestroyAPIView.as_view(), name='movie-retrieve-update-destroy'),
    # GET, PUT, DELETE for specific movie
    path('movies/<int:pk>/get/', MovieRetrieveUpdateDestroyAPIView.as_view(), name='movie-retrieve'),
    # GET for a single movie
    path('movies/<int:pk>/put/', MovieRetrieveUpdateDestroyAPIView.as_view(), name='movie-update'),  # PUT for updating
    path('movies/<int:pk>/delete/', MovieRetrieveUpdateDestroyAPIView.as_view(), name='movie-delete'),
    # DELETE for deleting

    # Category Endpoints
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    # GET for listing and POST for creating
    path('categories/get/', CategoryListCreateAPIView.as_view(), name='category-list'),  # GET for listing
    path('categories/post/', CategoryListCreateAPIView.as_view(), name='category-create'),  # POST for creating

    # Review Endpoints
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    # GET for listing and POST for creating
    path('reviews/get/', ReviewListCreateAPIView.as_view(), name='review-list'),  # GET for listing reviews
    path('reviews/post/', ReviewListCreateAPIView.as_view(), name='review-create'),  # POST for creating reviews

    # Watchlist Endpoints
    path('watchlist/', WatchlistRetrieveAPIView.as_view(), name='watchlist-retrieve'),  # GET for retrieving watchlist
    path('watchlist/get/', WatchlistRetrieveAPIView.as_view(), name='watchlist-retrieve-get'),
    # GET for retrieving watchlist
    path('watchlist/add/', WatchlistAddMovieAPIView.as_view(), name='watchlist-add'),
    # POST for adding movie to watchlist
    path('watchlist/remove/', WatchlistRemoveMovieAPIView.as_view(), name='watchlist-remove'),
    # POST for removing movie from watchlist
    path('', MovieListView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),  # `pk` for CBVs
    path('movie/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movie/<int:pk>/update/', MovieUpdateView.as_view(), name='movie_update'),
    path('movie/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie_delete'),

    # These can remain as function-based views (FBVs) for now
    path('movie/<int:movie_id>/review/', review_create, name='review_create'),
    path('movie/<int:movie_id>/upload_poster/', upload_poster, name='upload_poster'),

    # Auth views
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('accounts/signup/', auth_views.LoginView.as_view(template_name='registration/signup.html'), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]
