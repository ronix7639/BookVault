import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book
from .forms import BookForm

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
    with open('D:\\Rohit\\Career\\My Projects\\Python\\LibraryManagementSystem\\books.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) == 5:
                _, created = Book.objects.get_or_create(
                    title=row[0],
                    author=row[1],
                    category=row[2],
                    isbn=row[3],
                    quantity=row[4]
                )

    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully.')
            return redirect('BOOKS:dashboard')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form, 'operation': 'Add'})

@login_required
def book_update(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('BOOKS:dashboard')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'operation': 'Edit'})

@login_required
def book_delete(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('BOOKS:dashboard')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful.')
            return redirect('BOOKS:user_login')
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
    books = Book.objects.all()  
    return render(request, 'books/dashboard.html', {'books': books})

def home(request):
    return render(request, 'home.html')
