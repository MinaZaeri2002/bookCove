from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image
import os


User = get_user_model()


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='ژانر کتاب',
    )

    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='آدرس کوتاه'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='توضیحات'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    class Meta:
        verbose_name = 'ژانر'
        verbose_name_plural = 'ژانرها'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Author(models.Model):
    first_name = models.CharField(
        max_length=50,
        verbose_name='نام'
    )

    last_name = models.CharField(
        max_length=50,
        verbose_name='نام خانوادگی'
    )

    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='بیوگرافی'
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاریخ تولد'
    )

    death_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاریخ فوت'
    )

    nationality = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='ملیت'
    )

    photo = models.ImageField(
        upload_to='authors/',
        blank=True,
        null=True,
        verbose_name='عکس نویسنده'
    )

    website = models.URLField(
        blank=True,
        null=True,
        verbose_name='وبسایت'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسندگان'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_books_count(self):
        return self.books.count()


class Publisher(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='انتشارات'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='توضیحات'
    )

    website = models.URLField(
        blank=True,
        null=True,
        verbose_name='وبسایت'
    )

    established_year = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='سال تاسیس'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    class Meta:
        verbose_name = 'انتشارات'
        verbose_name_plural = 'انتشارات'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    LANGUAGE_CHOICES = [
        ('fa', 'فارسی'),
        ('en', 'انگلیسی'),
        ('ar', 'عربی'),
        ('fr', 'فرانسوی'),
        ('de', 'آلمانی'),
        ('other', 'سایر'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='عنوان کتاب'
    )

    subtitle = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='زیر عنوان'
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='آدرس کوتاه'
    )

    authors = models.ManyToManyField(
        Author,
        related_name='books',
        verbose_name='نویسندگان'
    )

    genres = models.ManyToManyField(
        Genre,
        related_name='books',
        verbose_name='ژانرها'
    )

    publisher = models.ForeignKey(
        Publisher,
        related_name='books',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='انتشارات'
    )

    description = models.TextField(
        verbose_name='توضیحات'
    )

    isbn = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        unique=True,
        verbose_name='شابک'
    )

    pages = models.PositiveIntegerField(
        verbose_name='تعداد صفحات'
    )

    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='fa',
        verbose_name='زبان'
    )

    publication_date = models.DateField(
        verbose_name='تاریخ انتشار'
    )

    cover_image = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True,
        verbose_name='کاور کتاب'
    )

    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        verbose_name='میانگین امتیاز'
    )

    total_ratings = models.PositiveIntegerField(
        default=0,
        verbose_name='تعداد ارزیابی‌ها'
    )

    total_reviews = models.PositiveIntegerField(
        default=0,
        verbose_name='تعداد نقدها'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='آخرین بروزرسانی'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب‌ها'
        ordering = ['-created_at', 'title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['isbn']),
            models.Index(fields=['average_rating']),
        ]

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        if self.cover_image:
            img = Image.open(self.cover_image)
            if img.height > 500 or img.width > 400:
                output_size = (400, 500)
                img.thumbnail(output_size)
                img.save(self.cover_image)

    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'slug': self.slug})

    def get_authors_name(self):
        return ", ".join([author.get_full_name() for author in self.authors.all()])

    def get_genre_name(self):
        return ", ".join([genre.name for genre in self.genres.all()])

    def update_rating(self):
        ratings = self.ratings.all()
        if ratings:
            total = sum([rating.score for rating in ratings])
            self.average_rating = total / len(ratings)
            self.total_ratings = len(ratings)

        else:
            self.average_rating = 0.00
            self.total_ratings = 0

        self.save(update_fields=['average_rating', 'total_ratings'])

    def update_reviews_count(self):
        self.total_reviews = self.reviews.count()
        self.save(update_fields=['total_reviews'])


class UserBook(models.Model):

    STATUS_CHOICES = [
        ('want_to_read', 'می‌خواهم بخوانم'),
        ('currently_reading', 'در حال خواندن'),
        ('read', 'خوانده شده'),
        ('did_not_finish', 'نیمه‌تمام'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_books',
        verbose_name='کاربر'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='user_books',
        verbose_name='کتاب'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name='وضعیت'
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ اضافه شدن'
    )

    date_started = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاریخ شروع خواندن'
    )

    date_ended = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاریخ اتمام خواندن'
    )

    current_page = models.PositiveIntegerField(
        default=0,
        verbose_name='صفحه فعلی'
    )

    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت‌ها'
    )

    class Meta:
        verbose_name = 'کاربر-کتاب:وضعیت'
        verbose_name_plural = 'کاربران-کتاب‌ها:وضعیت'
        unique_together = ('user', 'book')
        ordering = ['-date_ended']

    def __str__(self):
        return f'{self.user.username} {self.book.title}'

    def get_reading_progress(self):
        if self.book.pages > 0:
            return min(100, (self.current_page // self.book.pages) * 100)
        return 0


class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name='کاربر'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name='کتاب'
    )

    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='امتیاز'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='آخرین بروزرسانی'
    )

    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازات'
        unique_together = ('user', 'book')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.update_rating()


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='کاربر'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='کتاب'
    )

    title = models.CharField(
        max_length=100,
        verbose_name='عنوان نقد'
    )

    content = models.TextField(
        verbose_name='متن نقد'
    )

    is_spoiler = models.BooleanField(
        default=False,
        verbose_name='حاوی اسپویل'
    )

    is_approved = models.BooleanField(
        default=True,
        verbose_name='تایید شده'
    )

    likes_count = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد لایک‌ها"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی"
    )

    class Meta:
        verbose_name = "نقد"
        verbose_name_plural = "نقدها"
        unique_together = ['user', 'book']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.book.title}: {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.update_reviews_count()


class ReviewLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="نقد"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ لایک"
    )

    class Meta:
        verbose_name = "لایک نقد"
        verbose_name_plural = "لایک‌های نقدها"
        unique_together = ['user', 'review']

    def __str__(self):
        return f"{self.user.username} liked {self.review.title}"


