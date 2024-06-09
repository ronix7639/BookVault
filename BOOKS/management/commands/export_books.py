# import csv
# from django.core.management.base import BaseCommand
# from BOOKS.models import Book

# class Command(BaseCommand):
#     help = 'Export book data to a CSV file'

#     def add_arguments(self, parser):
#         parser.add_argument('filename', type=str, help='The CSV file to export to')

#     def handle(self, *args, **kwargs):
#         filename = kwargs['filename']

#         fieldnames = ['title', 'author', 'category', 'isbn', 'quantity']

#         with open(filename, 'w', newline='', encoding='utf-8') as file:
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             writer.writeheader()

#             books = Book.objects.all()
#             for book in books:
#                 writer.writerow({
#                     'title': book.title,
#                     'author': book.author,
#                     'category': book.category,
#                     'isbn': book.isbn,  
#                     'quantity': book.quantity
#                 })

#         self.stdout.write(self.style.SUCCESS(f'Book data exported to {filename}'))

from django.core.management.base import BaseCommand
from BOOKS.models import Book
import csv

class Command(BaseCommand):
    help = 'Export books to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        books = Book.objects.all()

        with open(csv_file, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['title', 'author', 'category', 'isbn', 'quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()

            for book in books:
                writer.writerow({
                    'title': book.title,
                    'author': book.author,
                    'category': book.category,
                    'isbn': book.isbn,
                    'quantity': book.quantity
                })

        self.stdout.write(self.style.SUCCESS(f"Successfully exported books to '{csv_file}'"))
