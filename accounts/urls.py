from django.urls import path
from .views import (
    SignUpView, CustomLoginView, CustomLogoutView,
    UserProfileEditView, UserProfileDetailView
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile_edit/<str:username>/', UserProfileEditView.as_view(), name='profile_edit'),
    path('profile_detail/<str:username>/', UserProfileDetailView.as_view(), name='profile_detail'),
]

