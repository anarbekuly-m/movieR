from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Prefetch
from .models import Movie, Category, Review, Watchlist
from .serializer import MovieSerializer, CategorySerializer, ReviewSerializer, WatchlistSerializer
from django.shortcuts import get_object_or_404

# Movie Endpoints

class MovieListCreateAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()

    # Prefetch related category and reviews for movies to avoid N+1 problem
    def get_queryset(self):
        return Movie.objects.prefetch_related(
            Prefetch('category'),
            Prefetch('reviews')
        )

    serializer_class = MovieSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class MovieRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()

    def get_queryset(self):
        return Movie.objects.prefetch_related(
            Prefetch('category'),
            Prefetch('reviews')
        )

    serializer_class = MovieSerializer

# Category Endpoints

class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# Review Endpoints

class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()

    # Prefetch related movie data for each review to avoid N+1 problem
    def get_queryset(self):
        return Review.objects.prefetch_related(
            Prefetch('movie')
        )

    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# Watchlist Endpoints

class WatchlistRetrieveAPIView(APIView):
    # Fetch the watchlist and related movies
    def get(self, request, *args, **kwargs):
        user = request.user
        watchlist = Watchlist.objects.prefetch_related(
            Prefetch('movies')
        ).get(user=user)

        serializer = WatchlistSerializer(watchlist)
        return Response(serializer.data)

class WatchlistAddMovieAPIView(APIView):
    def post(self, request, *args, **kwargs):
        movie_id = request.data.get('movie_id')
        movie = get_object_or_404(Movie, id=movie_id)
        user = request.user

        # Add the movie to the user's watchlist
        watchlist, created = Watchlist.objects.get_or_create(user=user)
        watchlist.movies.add(movie)

        return Response({"message": "Movie added to watchlist."}, status=status.HTTP_201_CREATED)

class WatchlistRemoveMovieAPIView(APIView):
    def post(self, request, *args, **kwargs):
        movie_id = request.data.get('movie_id')
        movie = get_object_or_404(Movie, id=movie_id)
        user = request.user

        # Remove the movie from the user's watchlist
        watchlist = Watchlist.objects.get(user=user)
        watchlist.movies.remove(movie)

        return Response({"message": "Movie removed from watchlist."}, status=status.HTTP_204_NO_CONTENT)
