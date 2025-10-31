# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from .forms import UserRegisterForm
from django.db import IntegrityError, DataError
from django.core.exceptions import ValidationError
from .models import Post
from django.http import JsonResponse
import re
from mixin_app.models import User
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.generics import GenericAPIView

# Protected page: only logged-in users can see

class ValidateData(GenericAPIView):
    def validate_email(user_email):
            email = user_email or ""
            try:
                email_name, domain_part = email.strip().rsplit("@", 1)
            except ValueError:
                raise ValueError("Invalid email format: missing '@' symbol")
            
            else:
                email = email_name + "@" + domain_part.lower()
            return email
    
    def validate_mobile(mobile_no):
        mobile = str(mobile_no or "").strip()
        pattern = r'^[6-9]\d{9}$'  

        if not re.match(pattern, mobile):
            raise ValueError("Invalid mobile number: must be 10 digits and start with 6-9.")

        return mobile
    
    def validate_username(username):
        username = (username or "").strip()

        pattern = r'^[A-Za-z0-9_]{3,20}$'

        if re.match(pattern, username):
            return username
        else:
            return None 
        
class RegisterView(ValidateData):
    def post(self, request):
        username = request.data.get('username')
        user_email = request.data.get('email')
        password = request.data.get('password')
        phone_number = request.data.get('phone_no')
        address = request.data.get('address')
        
        
        clean_email = ValidateData.validate_email(user_email)
        clean_mobile_no = ValidateData.validate_mobile(phone_number)
        clean_username = ValidateData.validate_username(username)
        try:
            user = User.objects.create(
                email = clean_email,
                phone_no = clean_mobile_no,
                username = clean_username,
                address = address,
                password = password
            )
        except (ValueError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=400)
            
        except IntegrityError as e:
            return JsonResponse({'error': f'Duplicate entry for the key : {user_email}'})    
    
        except DataError as e:
            return JsonResponse({'error': 'Invalid data length or format — please check your input fields.'}, status=400)    
        
        data = {
                'message': 'Success',
                'status': 200,
                'data': {
                    
                    'username': user.username,
                    'email': user.email,
                }
            }
        return JsonResponse(data)


# Registration view
class RegistereView(View):
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