from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)  
    def __str__(self):
        return self.username
    
class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE) 

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)  
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  
    content = models.TextField()  
    timestamp = models.DateTimeField(auto_now_add=True)  
