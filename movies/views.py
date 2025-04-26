from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Movie
from .forms import MovieForm, ReviewForm, MoviePosterForm


# 🎬 Movie List View
class MovieListView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'

    def get(self, request, *args, **kwargs):
        request.session['last_viewed'] = 'Movie List'
        return super().get(request, *args, **kwargs)


# 🎬 Movie Detail View
class MovieDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'
    permission_required = 'movies.view_movie'

    def get_object(self, queryset=None):
        movie = super().get_object(queryset)
        self.request.session['last_viewed_movie'] = movie.id
        return movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        return context


# 🎬 Create Movie
class MovieCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/movie_form.html'
    permission_required = 'movies.add_movie'
    success_url = reverse_lazy('movie_list')


# 🎬 Update Movie
class MovieUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/movie_form.html'
    permission_required = 'movies.change_movie'
    success_url = reverse_lazy('movie_list')


# 🎬 Delete Movie
class MovieDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Movie
    template_name = 'movies/movie_confirm_delete.html'
    permission_required = 'movies.delete_movie'
    success_url = reverse_lazy('movie_list')


# ⭐ Review Create View (FBV for now)
from django.contrib.auth.decorators import login_required

@login_required
def review_create(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_detail', pk=movie.id)
    else:
        form = ReviewForm()
    return render(request, 'movies/review_form.html', {'form': form})


# 🖼 Upload Poster (FBV for now)
@login_required
def upload_poster(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        form = MoviePosterForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', pk=movie.id)
    else:
        form = MoviePosterForm(instance=movie)
    return render(request, 'movies/upload_poster.html', {'form': form, 'movie': movie})
