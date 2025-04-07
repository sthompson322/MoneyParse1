from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
    path('profile', views.profile, name='home.profile'),
    path('chatbot', views.chatbot_view, name='home.chatbot'),
]