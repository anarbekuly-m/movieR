from rest_framework import serializers
from .models import Movie, Category, Review, Watchlist, Rating
from datetime import date


# Category Serializer (using serializers.Serializer)
class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)

    def validate_name(self, value):
        # Ensure that category name is not empty and doesn't contain special characters
        if not value.strip():
            raise serializers.ValidationError("Category name cannot be empty.")
        if not value.isalnum():
            raise serializers.ValidationError("Category name must contain only alphanumeric characters.")
        return value

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


# Movie Serializer (using serializers.Serializer)
class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    release_date = serializers.DateField()
    director = serializers.CharField(max_length=100)
    poster = serializers.ImageField(required=False)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.SerializerMethodField()

    def validate_release_date(self, value):
        # Ensure that the release date is not in the future
        if value > date.today():
            raise serializers.ValidationError("Release date cannot be in the future.")
        return value

    def get_average_rating(self, obj):
        # Calculate average rating (if any reviews exist)
        reviews = obj.reviews.all()
        if reviews:
            return sum([review.rating for review in reviews]) / len(reviews)
        return 0

    def create(self, validated_data):
        category = validated_data.pop('category', None)
        movie = Movie.objects.create(**validated_data)
        return movie

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.director = validated_data.get('director', instance.director)
        instance.save()
        return instance


# Review Serializer (using serializers.Serializer)
class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), write_only=True)
    rating = serializers.IntegerField()
    review_text = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    def validate_rating(self, value):
        # Ensure that the rating is within the valid range (1-5)
        if value not in [1, 2, 3, 4, 5]:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_review_text(self, value):
        # Ensure that the review text is not empty
        if not value.strip():
            raise serializers.ValidationError("Review text cannot be empty.")
        return value

    def create(self, validated_data):
        review = Review.objects.create(**validated_data)
        return review

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.review_text = validated_data.get('review_text', instance.review_text)
        instance.save()
        return instance


# Watchlist Serializer (using serializers.Serializer)
class WatchlistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    movies = MovieSerializer(many=True, read_only=True)

    def validate_movies(self, value):
        # Ensure that the movies in the watchlist exist
        if not value:
            raise serializers.ValidationError("Watchlist cannot be empty.")
        for movie in value:
            if not Movie.objects.filter(id=movie.id).exists():
                raise serializers.ValidationError(f"Movie with ID {movie.id} does not exist.")
        return value

    def create(self, validated_data):
        watchlist = Watchlist.objects.create(**validated_data)
        return watchlist

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance
