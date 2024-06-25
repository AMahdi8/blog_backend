from django.urls import path, include

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('last-post/', last_posts, name='5-last-post'),
    path('categories/', categories, name='categories')
]
