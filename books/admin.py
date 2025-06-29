from django.contrib import admin
from django.utils.html import format_html
from .models import Genre, Author, Publisher, Book, UserBook, Rating, Review, ReviewLike


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'books_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']

    def books_count(self, obj):
        return obj.books.count()
    books_count.short_description = 'تعداد کتاب‌ها'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'nationality', 'birth_date', 'books_count', 'created_at']
    list_filter = ['nationality', 'birth_date', 'created_at']
    search_fields = ['first_name', 'last_name']
    readonly_fields = ['created_at']

    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('first_name', 'last_name', 'nationality', 'birth_date', 'death_date')
        }),
        ('جزئیات', {
            'fields': ('bio', 'photo', 'website')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at',)
        }),
    )

    def books_count(self, obj):
        return obj.get_books_count()
    books_count.short_description = 'تعداد کتاب‌ها'


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'established_year', 'books_count', 'created_at']
    list_filter = ['established_year', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']

    def books_count(self, obj):
        return obj.books_count()
    books_count.short_description = 'تعداد کتاب‌ها'


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    fields = ['user', 'title', 'is_approved', 'is_spoiler', 'likes_count']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'get_authors', 'publisher', 'language',
        'average_rating', 'total_ratings', 'total_reviews',
        'publication_date', 'is_active'
    ]
    list_filter = [
        'language', 'genres', 'publication_date',
        'is_active', 'created_at'
    ]
    search_fields = ['title', 'subtitle', 'isbn', 'authors__first_name', 'authors__last_name']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'average_rating', 'total_ratings', 'total_reviews',
        'created_at', 'updated_at', 'cover_preview'
    ]

    filter_horizontal = ['authors', 'genres']
    inlines = [RatingInline, ReviewInline]

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'subtitle', 'slug', 'authors', 'genres', 'publisher')
        }),
        ('جزئیات کتاب', {
            'fields': ('description', 'isbn', 'pages', 'language', 'publication_date')
        }),
        ('تصاویر', {
            'fields': ('cover_image', 'cover_preview')
        }),
        ('آمار', {
            'fields': ('average_rating', 'total_ratings', 'total_reviews')
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_authors(self, obj):
        return obj.get_authors_names()

    get_authors.short_description = 'نویسندگان'

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 150px;"/>',
                obj.cover_image.url
            )
        return "بدون تصویر"

    cover_preview.short_description = 'پیش‌نمایش کاور'


@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'book', 'status', 'current_page',
        'get_reading_progress', 'date_added'
    ]
    list_filter = ['status', 'date_added', 'date_started', 'date_finished']
    search_fields = ['user__username', 'book__title']
    readonly_fields = ['date_added']

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('user', 'book', 'status')
        }),
        ('پیشرفت خواندن', {
            'fields': ('current_page', 'date_started', 'date_finished')
        }),
        ('یادداشت‌ها', {
            'fields': ('notes',)
        }),
        ('تاریخ‌ها', {
            'fields': ('date_added',)
        }),
    )

    def get_reading_progress(self, obj):
        progress = obj.get_reading_progress()
        return f"{progress:.1f}%"

    get_reading_progress.short_description = 'پیشرفت خواندن'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'score', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['user__username', 'book__title']
    readonly_fields = ['created_at', 'updated_at']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['user', 'book']
        return self.readonly_fields


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'user', 'book', 'is_approved',
        'is_spoiler', 'likes_count', 'created_at'
    ]
    list_filter = ['is_approved', 'is_spoiler', 'created_at']
    search_fields = ['title', 'content', 'user__username', 'book__title']
    readonly_fields = ['likes_count', 'created_at', 'updated_at']

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('user', 'book', 'title')
        }),
        ('محتوای نقد', {
            'fields': ('content',)
        }),
        ('تنظیمات', {
            'fields': ('is_approved', 'is_spoiler')
        }),
        ('آمار', {
            'fields': ('likes_count',)
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    actions = ['approve_reviews', 'disapprove_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} نقد تایید شد.")

    approve_reviews.short_description = "تایید نقدهای انتخاب شده"

    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} نقد رد شد.")

    disapprove_reviews.short_description = "رد نقدهای انتخاب شده"


@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'review__title']
    readonly_fields = ['created_at']

