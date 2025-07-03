from django.urls import path
from .views import HomeView, BookSearchView, GenreListView, AuthorListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('book_search/', BookSearchView.as_view(), name='book_search'),
    path('genre_list/', GenreListView.as_view(), name='genre_list'),
    path('author_list/', AuthorListView.as_view(), name='author_list'),
]