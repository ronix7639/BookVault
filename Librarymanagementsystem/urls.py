from django.urls import path, include
from BOOKS.views import user_login, register, user_logout, home
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('BOOKS.urls')),
    path('user_login/', user_login, name='user_login'), 
    path('register/', register, name='register'), 
    path('user_logout/', user_logout, name='user_logout'),
    path('', home, name='home'),
]
