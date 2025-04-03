from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
    path('reports', views.reports, name='home.reports'),
    path('budget', views.budget, name='home.budget'),
    path('profile', views.profile, name='home.profile'),
]