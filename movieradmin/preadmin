from django.contrib import admin
from movies.models import Movie, Category, Review, Watchlist

# Custom Admin Panel Header & Titles
class MovieRAdmin(admin.AdminSite):
    site_header = "🎬 MovieR Admin Panel"
    site_title = "MovieR Admin"
    index_title = "Welcome to MovieR Admin"

# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Movie Admin
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'director', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'director')
    list_editable = ('category',)

# Review Admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    search_fields = ('movie__title', 'user__username')
    list_filter = ('rating',)

# Watchlist Admin
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user',)

# Register models to the custom admin site
admin_site = MovieRAdmin(name="movieradmin")
admin_site.register(Category, CategoryAdmin)
admin_site.register(Movie, MovieAdmin)
admin_site.register(Review, ReviewAdmin)
admin_site.register(Watchlist, WatchlistAdmin)
