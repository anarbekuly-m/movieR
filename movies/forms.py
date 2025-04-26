from django import forms
from .models import Movie, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'director', 'category', 'poster']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']



class MoviePosterForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['poster']
