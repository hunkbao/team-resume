from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.verify, name='verify'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]
