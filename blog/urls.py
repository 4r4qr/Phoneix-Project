from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('like/', views.like_post, name='like_post'),
    path('search/', views.search, name='search'),
    path('curriculum/', views.curriculum_view, name='curriculum'),
    path('smart-tools/', views.smart_tools_view, name='smart_tools'),
    path('phone-security/', views.phone_security_view, name='phone_security'),
]
