# models.py
from django.db import models

class User(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=30, null=True)
    email=models.EmailField(unique=True)
    phone_no=models.CharField(max_length=10, null=True)
    password=models.CharField(max_length=100, null=True)
    address=models.CharField(max_length=255, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='user'
    
    def __str__(self):
        return f"{self.username}"    
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='posts'
    def __str__(self):
        return self.title
