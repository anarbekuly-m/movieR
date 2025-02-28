from django.contrib import admin
from .models import Movie, Review, Category, Watchlist

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Watchlist)
