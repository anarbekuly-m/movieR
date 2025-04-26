from django.core.management.base import BaseCommand
import csv
from movies.models import Movie, Category, Review

class Command(BaseCommand):
    help = "Import movies and reviews from CSV files"

    def handle(self, *args, **kwargs):
        try:
            # Import Categories first
            category_dict = {}

            with open('movies_data.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    category_name = row['category'].strip()
                    if category_name not in category_dict:
                        category, created = Category.objects.get_or_create(name=category_name)
                        category_dict[category_name] = category
                        self.stdout.write(self.style.SUCCESS(f"Category added: {category_name}"))

            # Import Movies
            with open('movies_data.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    category = category_dict.get(row['category'].strip())

                    movie, created = Movie.objects.get_or_create(
                        title=row['title'],
                        defaults={
                            'description': row['description'],
                            'release_date': row['release_date'],
                            'director': row['director'],
                            'category': category
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Movie added: {movie.title}"))

            # Import Reviews
            with open('reviews_data.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        movie = Movie.objects.get(id=row['movie_id'])
                        Review.objects.create(
                            movie=movie,
                            rating=int(row['rating']),
                            review_text=row['review_text'],
                            created_at=row['created_at']
                        )
                        self.stdout.write(self.style.SUCCESS(f"Review added for: {movie.title}"))
                    except Movie.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Movie with ID {row['movie_id']} not found."))

            self.stdout.write(self.style.SUCCESS("✅ All data successfully imported!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))
