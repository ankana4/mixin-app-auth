# urls.py
from django.urls import path
from .views import PostListView, RegisterView, CustomLogoutView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
