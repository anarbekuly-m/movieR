# admin.py
from django.contrib import admin
from django.contrib.auth.models import User



from movies.models import Movie, Review, Category, Watchlist  # Import models from api_view.py

# Custom Admin Panel Header & Titles
class MovieRAdmin(admin.AdminSite):
    site_header = "🎬 MovieR Admin Panel"
    site_title = "MovieR Admin"
    index_title = "Welcome to MovieR Admin"


# Inline for Watchlist to show Movies in the Watchlist
class WatchlistInline(admin.TabularInline):
    model = Watchlist.movies.through  # This is the intermediate model for Many-to-Many relationship
    extra = 0  # Number of empty forms to display by default

# Admin class for Movie
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [WatchlistInline]


admin_site = MovieRAdmin(name="movieradmin")
admin_site.register(Category)
admin_site.register(Watchlist)
admin_site.register(Movie,MovieAdmin)
admin_site.register(Review)
admin_site.register(User)





