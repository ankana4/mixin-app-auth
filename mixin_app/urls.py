# urls.py
from django.urls import path
from .views import RegisterView, LoginView, CreatePostView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('posts/', CreatePostView.as_view(), name='create_post'),
]
