from rest_framework.permissions import IsAuthenticated, IsAdminUser
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
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Start with the base queryset
        queryset = Movie.objects.prefetch_related(
            Prefetch('category'),
            Prefetch('reviews')
        )

        # Get the query parameters for movie_id and category
        movie_id = self.request.query_params.get('id', None)
        category_name = self.request.query_params.get('category', None)

        #GET /movies/?id=12&category=Sci-Fi

        # Filter by movie ID if provided
        if movie_id:
            queryset = queryset.filter(id=movie_id)

        # Filter by category name if provided
        if category_name:
            queryset = queryset.filter(category__name=category_name)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MovieRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()

    def get_queryset(self):
        return Movie.objects.prefetch_related(
            Prefetch('category'),
            Prefetch('reviews')
        )

    serializer_class = MovieSerializer
    permission_classes = [IsAdminUser]


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
