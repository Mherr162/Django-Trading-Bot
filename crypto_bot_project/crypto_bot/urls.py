# crypto_bot/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.bot_control, name='bot_control'),
    path('logs/', views.get_logs, name='get_logs'),
]