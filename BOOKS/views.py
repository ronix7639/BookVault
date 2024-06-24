from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
import csv
from .models import Book, PastModification
from .forms import BookForm, ImportBooksForm
from .management.commands.import_books import Command  # Assuming you have a custom management command for importing books
from tempfile import NamedTemporaryFile


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('BOOKS:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form input.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def book_list(request):
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="books.csv"'

        writer = csv.writer(response)
        writer.writerow(['Title', 'Author', 'Category', 'ISBN', 'Quantity'])

        books = Book.objects.filter(user=request.user)  # Filter by logged-in user
        for book in books:
            writer.writerow([book.title, book.author, book.category, book.isbn, book.quantity])

        return response

    books = Book.objects.filter(user=request.user)  # Filter by logged-in user
    return render(request, 'books/book_list.html', {'books': books})



@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            messages.success(request, 'Book added successfully.')
            return redirect('BOOKS:dashboard')
    else:
        form = BookForm()
    return render(request, 'books/book_create.html', {'form': form, 'operation': 'Add'})


@login_required
def import_books_view(request):
    if request.method == 'POST':
        form = ImportBooksForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            # Check if the uploaded file is InMemoryUploadedFile or TemporaryUploadedFile
            if csv_file.multiple_chunks():
                # InMemoryUploadedFile: Small file that fits entirely in memory
                content = csv_file.read().decode('utf-8').splitlines()
                csv_reader = csv.DictReader(content)
            else:
                # TemporaryUploadedFile: Larger file that gets saved to disk
                with NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(csv_file.read())
                    temp_file_name = temp_file.name

                with open(temp_file_name, 'r', encoding='utf-8') as file:
                    csv_reader = csv.DictReader(file)

            # Get the logged-in user
            user = request.user

            command = Command()
            command.handle(csv_file=temp_file_name, user=user)  # Pass the user to the command

            messages.success(request, 'Books imported successfully.')
            
            return redirect('BOOKS:dashboard')  # Redirect to dashboard after import
    else:
        form = ImportBooksForm()
    
    return render(request, 'books/import_books.html', {'form': form})



@login_required
def book_update(request, id):
    book = get_object_or_404(Book, id=id, user=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            updated_book = form.save()

            # Record modification in PastModification
            PastModification.objects.create(user=request.user, book=updated_book)

            messages.success(request, 'Book updated successfully.')
            return redirect('BOOKS:dashboard')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_update.html', {'form': form, 'operation': 'Edit'})


@login_required
def book_delete(request, id):
    book = get_object_or_404(Book, id=id, user=request.user)
    if request.method == 'POST':
        if 'confirm_delete' in request.POST:
            book.delete()
            messages.success(request, 'Book deleted successfully.')
            return redirect('BOOKS:dashboard')
        else:
            # Handle the case if 'confirm_delete' is not in request.POST
            messages.error(request, 'Deletion confirmation not received.')
            return redirect('BOOKS:dashboard')
    return render(request, 'books/book_confirm_delete.html', {'book': book})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Add a success message to be shown in an alert
            messages.success(request, 'Registration successful.')
            return render(request, 'register.html', {'registered': True})  # Pass 'registered' as context
        else:
            messages.error(request, 'Registration failed. Please check the form for errors.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    auth_logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('BOOKS:user_login')


@login_required
def dashboard(request):
    books = Book.objects.filter(user=request.user)
    return render(request, 'books/dashboard.html', {'books': books})


def home(request):
    return render(request, 'home.html')
