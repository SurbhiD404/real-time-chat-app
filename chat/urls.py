from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ChatRoomViewSet


router = DefaultRouter()
router.register(r'rooms', ChatRoomViewSet, basename='room')


urlpatterns = [
    
    path('api/register/', RegisterView.as_view(), name='register'),  

   path('<str:room_name>/', views.chat_room, name='chat_room'),  
] + router.urls
    