# views.py
from django.db import IntegrityError, DataError
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
import re
import bcrypt
from mixin_app.models import User
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
    def hash_password(password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password
    
    def validate_mobile(mobile_no):
        mobile = str(mobile_no or "").strip()
        pattern = r'^[6-9]\d{9}$'  

        if not re.match(pattern, mobile):
            raise ValueError("Invalid mobile number: must be 10 digits and start with 6-9.")

        return mobile
        
class RegisterView(ValidateData):
    def post(self, request):
        username = request.data.get('username')
        user_email = request.data.get('email')
        password = request.data.get('password')
        phone_number = request.data.get('phone_no')
        address = request.data.get('address')
        
        
        clean_email = ValidateData.validate_email(user_email)
        clean_mobile_no = ValidateData.validate_mobile(phone_number)
        secure_password = ValidateData.hash_password(password)
        try:
            user = User.objects.create(
                email = clean_email,
                phone_no = clean_mobile_no,
                username = username,
                address = address,
                password = secure_password
            )
        except (ValueError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=400)
            
        except IntegrityError as e:
            return JsonResponse({'error': f'Duplicate entry for the key : {user_email}'})    
    
        except DataError as e:
            return JsonResponse({'error': 'Invalid data length or format — please check your input fields.'}, status=400)    
        print("userrr ", user.username)
        data = {
                'message': 'Success',
                'status': 200,
                'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }
        return JsonResponse(data)


class LoginView(ValidateData):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print("password ", password)
        
        if not username or not password:
            return JsonResponse({'error': 'Username or Password field is required.'}, status=400)

        try:
            user = User.objects.get(username=username)
            print("Password ", user.password)
        except User.DoesNotExist:
            return JsonResponse({'error':'Invalid username or password.'})   
        
        if check_password(password, user.password):
            
            return JsonResponse({
                'message': 'Login is successful',
                'sattus': 200,
                'data':{
                    'username': user.username,
                    'email': user.email,
                }
            })         
            
        else:
            return JsonResponse({'error': 'Invalid username or password'})

