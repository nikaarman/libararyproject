from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.author_list, name='author_list'),
    path('authors/create/', views.create_author, name='create_author'),
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.create_book, name='create_book'),
]