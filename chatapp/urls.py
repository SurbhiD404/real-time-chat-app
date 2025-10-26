"""
URL configuration for chatapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from chat.views import RegisterView, ChatRoomViewSet
from chat import views 

router = DefaultRouter()
router.register(r'rooms', ChatRoomViewSet, basename='room')  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  
    path('api/register/', RegisterView.as_view(), name='register'), 
    path('api/login/', TokenObtainPairView.as_view(), name='login'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
]
