from django.urls import path
from .views import (
    user_login, user_logout, register, dashboard,
    book_list, book_create, book_update, book_delete, home,
    import_books_view  # Import the new view for importing books
)

app_name = 'BOOKS'

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('books/', book_list, name='book_list'),
    path('books/add/', book_create, name='book_create'),
    path('books/<int:id>/edit/', book_update, name='book_update'),
    path('books/<int:id>/delete/', book_delete, name='book_delete'),
    path('books/import/', import_books_view, name='import_books'),  # New URL for importing books
    path('', home, name='home'),  
]
