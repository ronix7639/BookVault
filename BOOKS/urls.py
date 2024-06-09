from django.urls import path
from .views import (
    user_login, user_logout, register, dashboard,
    book_list, book_create, book_update, book_delete, home
)

app_name = 'BOOKS'

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('books/', book_list, name='book_list'),
    path('books/add/', book_create, name='book_create'),
    path('books/edit/<int:id>/', book_update, name='book_update'),
    path('books/delete/<int:id>/', book_delete, name='book_delete'),
    path('', home, name='home'),  
]
