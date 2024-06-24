import os
import csv
from django.core.management.base import BaseCommand
from BOOKS.models import Book

class Command(BaseCommand):
    help = 'Import books from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('user', type=str, help='Username of the user')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        user = kwargs['user']

        # Your CSV reading and book creation logic
        # Example:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                title = row['Title']
                author = row['Author']
                category = row['Category']
                isbn = row['ISBN']
                quantity = row['Quantity']

                # Create or update book associated with the user
                book, created = Book.objects.update_or_create(
                    title=title,
                    defaults={
                        'author': author,
                        'category': category,
                        'isbn': isbn,
                        'quantity': quantity,
                        'user': user  # Associate the book with the user
                    }
                )

                # Print or log information about the imported books
                self.stdout.write(self.style.SUCCESS(f'Updated quantity for book "{title}"'))

        # Clean up any temporary files if necessary
        if os.path.exists(csv_file):
            os.remove(csv_file)
