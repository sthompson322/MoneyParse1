from django.urls import path
from . import views

urlpatterns = [
    path('reports', views.reports_view, name='finances.reports'),
    path('budget', views.budget_view, name='finances.budget'),
    path('income', views.income_view, name="finances.income"),
    path('transactions', views.transactions_view, name="finances.transactions"),
    path('transactions-display', views.transactions_display, name="finances.transactions_display")
]
