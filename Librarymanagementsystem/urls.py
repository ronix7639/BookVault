from django.contrib import admin
from django.urls import path
from django.urls import include  # Import include to include app urls
from BOOKS import views  # Import views from your app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('BOOKS.urls')),  # Include your app urls
]