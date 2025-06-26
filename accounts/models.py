from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='ایمیل'
    )

    phone_number = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name='شماره تلفن',
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='درباره من',
    )

    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.jpg',
        verbose_name='عکس پروفایل'
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاریخ تولد'
    )

    profile_is_public = models.BooleanField(
        default=True,
        verbose_name='نمایش پروفایل'
    )

    show_email = models.BooleanField(
        default=False,
        verbose_name='نمایش ایمیل'
    )

    books_read_count = models.PositiveIntegerField(
        default=0,
        verbose_name='تعداد کتاب‌های خوانده شده'
    )

    reviews_count = models.PositiveIntegerField(
        default=0,
        verbose_name='تعداد نقدهای نوشته شده'
    )

    yearly_reading_goal = models.PositiveIntegerField(
        default=12,
        verbose_name='هدف مطالعه سالانه'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ عضویت'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='آخرین بروزرسانی'
    )

    favorite_genres = models.ManyToManyField(
        'books.Genre',
        blank=True,
        verbose_name='ژانرهای مورد علاقه'
    )

    website = models.URLField(
        blank=True,
        null=True,
        verbose_name='وبسایت'
    )

    instagram = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='اینستاگرام'
    )

    telegram = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='تلگرام'
    )

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.username} - {self.email}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_picture:
            img = Image.open(self.profile_picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)

    def get_full_name_or_username(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return f'{self.username}'

    def get_reading_progress(self):
        if self.yearly_reading_goal == 0:
            return 0
        return min(100, (self.books_read_count // self.yearly_reading_goal) * 100)

    def update_books_count(self):
        from books.models import UserBook
        self.books_read_count = UserBook.objects.filter(
            user=self,
            status='read',
        ).count()
        self.save(update_fields=['books_read_count'])

    def update_reviews_count(self):
        from books.models import Review
        self.reviews_count = Review.objects.filter(user=self).count()
        self.save(update_fields=['reviews_count'])


