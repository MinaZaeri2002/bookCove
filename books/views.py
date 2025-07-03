from re import search

from django.db.models import Q, Count, Avg
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import Book, Genre, Author


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['latest_books'] = Book.objects.filter(is_active=True).order_by('-created_at')[:8]
        context['popular_books'] = Book.objects.filter(is_active=True).order_by('-average_rating')[:8]
        context['top_rated_books'] = Book.objects.filter(is_active=True, average_rating__gte=4.0).order_by('-average_rating')[:8]
        context['popular_genres'] = Genre.objects.annotate(
            books_count=Count('books', filter=Q(books__is_active=True)),
        ).filter(books_count__gt=0).order_by('-books_count')[:8]
        context['popular_authors'] = Author.objects.annotate(
            books_count=Count('books', filter=Q(books__is_active=True)),
        ).filter(books_count__gt=0).order_by('-books_count')[:8]

        context['stats'] = {
            'total_books': Book.objects.filter(is_active=True).count(),
            'total_authors': Author.objects.filter(books__is_active=True).distinct().count(),
            'total_genres': Genre.objects.filter(books__is_active=True).distinct().count(),
            'avg_rating': Book.objects.filter(is_active=True, average_rating__isnull=False).aggregate(
                avg=Avg('average_rating')
            )['avg'] or 0
        }

        return context


class BookSearchView(ListView):
    model = Book
    template_name = 'book_search.html'
    paginate_by = 24
    context_object_name = 'books'

    def get_queryset(self):
        queryset = Book.objects.filter(is_active=True)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(authors__first_name__icontains=search_query) |
                Q(authors__last_name__icontains=search_query) |
                Q(isbn__icontains=search_query)
            ).distinct()

        genre_slug = self.request.GET.get('genre')
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)

        min_rating = self.request.GET.get('min_rating')
        if min_rating:
            try:
                min_rating = float(min_rating)
                queryset = queryset.filter(average_rating__gte=min_rating)
            except ValueError:
                pass

        author_id = self.request.GET.get('author')
        if author_id:
            try:
                queryset = queryset.filter(authors__author_id=author_id)
            except ValueError:
                pass

        sort_by = self.request.GET.get('sort_by', '-created_at')
        if sort_by == 'title':
            queryset = queryset.order_by('title')
        elif sort_by == 'popular':
            queryset = queryset.order_by('-average_rating')
        elif sort_by == 'rating':
            queryset = queryset.order_by('-average_rating')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset.select_related('publisher').prefetch_related('authors', 'genres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['genres'] = Genre.objects.all()
        context['authors'] = Author.objects.all()

        context['search_params'] = self.request.GET.copy()
        if 'page' in context['search_params']:
            del context['search_params']['page']

        context["search_query"] = self.request.GET.get('q', '')
        context['has_search'] = bool(
            self.request.GET.get('q') or
            self.request.GET.get('genre') or
            self.request.GET.get('min_rating') or
            self.request.GET.get('author')
        )

        genre_slug = self.request.GET.get('genre')
        if genre_slug:
            try:
                genre = Genre.objects.get(slug=genre_slug)
                context['genre_name'] = genre.name
            except Genre.DoesNotExist:
                pass

        author_id = self.request.GET.get('author')
        if author_id:
            try:
                author = Author.objects.get(id=author_id)
                context['author_name'] = f"{author.first_name} {author.last_name}"
            except Author.DoesNotExist:
                pass

        return context


class GenreListView(ListView):
    model = Genre
    template_name = 'genres.html'
    context_object_name = 'genres'

    def get_queryset(self):
        return Genre.objects.annotate(
            books_count=Count('books', filter=Q(books__is_active=True))
        ).filter(books_count__gt=0).order_by('-books_count')



class AuthorListView(ListView):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'authors'

    def get_queryset(self):
        return Author.objects.annotate(
            books_count=Count('books', filter=Q(books__is_active=True))
        ).filter(books_count__gt=0).order_by('-books_count')