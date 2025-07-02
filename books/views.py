from re import search

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from .models import Book, Genre


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    paginate_by = 24

    def get_queryset(self):
        queryset = Book.objects.filter(is_active=True)
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(authors__first_name__icontains=search_query) |
                Q(authors__last_name__icontains=search_query) |
                Q(isbn__icontains=search_query)
            )

        genre_slug = self.request.GET.get("genre")
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)

        min_rating = self.request.GET.get("min_rating")
        if min_rating:
            queryset = queryset.filter(average_rating__gte=min_rating)

        sort_by = self.request.GET.get("sort_by", "-created_at")
        if sort_by == 'title':
            queryset = queryset.order_by('title')
        elif sort_by == 'popular':
            queryset = queryset.order_by('-total_rating')
        elif sort_by == 'rating':
            queryset = queryset.order_by('-average_rating')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset.select_related("publisher").prefetch_related("authors", "genres")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()

        context["search_params"] = self.request.GET.copy()
        if "page" in context["search_params"]:
            del context["search_params"]["page"]

        return context