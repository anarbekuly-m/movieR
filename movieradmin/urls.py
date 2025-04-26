from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('movieradmin/', admin.site.urls),  # Change default /admin/ to /movieradmin/
]
