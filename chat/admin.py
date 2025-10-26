from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ChatRoom, Message


admin.site.register(User, UserAdmin)


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_by']  
    search_fields = ['name']  
    list_filter = ['created_by']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'sender', 'content', 'timestamp']  
    search_fields = ['content']   
    list_filter = ['room', 'sender']  

