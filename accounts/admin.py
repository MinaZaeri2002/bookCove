from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'books_read_count', 'reviews_count', 'is_active', 'created_at'
    ]

    list_filter = [
        'is_active', 'is_staff', 'is_superuser',
        'profile_is_public', 'created_at'
    ]

    search_fields = ['username', 'email', 'first_name', 'last_name']

    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'updated_at', 'books_read_count', 'reviews_count')

    fieldsets = UserAdmin.fieldsets + (
        ('اظلاعات شخصی', {
            'fields': (
                'phone_number', 'bio', 'profile_picture', 'birth_date'
            )
        }),
        ('تنظیمات حریم خصوصی', {
            'fields': (
                'profile_picture', 'show_email'
            )
        }),
        ('آمار', {
            'fields': (
                'books_read_count', 'reviews_count', 'yearly_reading_goal'
            )
         }),
        ('شبکه‌های اجتماعی', {
            'fields': (
                'website', 'instagram', 'telegram'
            )
        }),
        ('تاریخ‌ها', {
            'fields': (
                'created_at', 'updated_at'
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name',
                'password1', 'password2'
            ),
        }),
    )
