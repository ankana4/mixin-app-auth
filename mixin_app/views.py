# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from .forms import UserRegisterForm
from .models import Post
# Login view (using built-in)
from django.contrib.auth.views import LoginView, LogoutView

# Protected page: only logged-in users can see
class PostListView(LoginRequiredMixin, TemplateView):
    template_name = 'posts.html'
    login_url = '/login/' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        print("Hii", context)
        return context


# Registration view
class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('post-list')
        return render(request, 'register.html', {'form': form})



class CustomLogoutView(LogoutView):
    next_page = '/login/'  # Redirect after logout