from django.core.management.base import BaseCommand
from BOOKS.models import Book
import csv

class Command(BaseCommand):
    help = 'Import books from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                title = row.get('title')
                author = row.get('author')
                category = row.get('category')
                isbn = row.get('isbn')
                quantity = row.get('quantity')

                # Check if the quantity value is missing
                if not quantity:
                    self.stdout.write(self.style.WARNING(f"Missing quantity value for book '{title}'"))
                    continue

                try:
                    quantity = int(quantity)
                except ValueError:
                    self.stdout.write(self.style.WARNING(f"Invalid quantity value for book '{title}'"))
                    continue

                # Check if a book with the same ISBN already exists
                existing_book = Book.objects.filter(isbn=isbn).first()
                if existing_book:
                    # If the book already exists, update its quantity
                    existing_book.quantity += quantity
                    existing_book.save()
                    self.stdout.write(self.style.SUCCESS(f"Successfully updated quantity for book '{title}'"))
                else:
                    # If the book does not exist, create a new entry
                    book = Book(title=title, author=author, category=category, isbn=isbn, quantity=quantity)
                    book.save()
                    self.stdout.write(self.style.SUCCESS(f"Successfully imported book '{title}'"))
