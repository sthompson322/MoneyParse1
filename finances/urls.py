from django.urls import path
from . import views

urlpatterns = [
    path('reports', views.reports_view, name='finances.reports'),
    path('budget', views.budget_view, name='finances.budget'),
    path('income', views.income_view, name="finances.income"),
    path('transactions', views.transactions_view, name="finances.transactions"),
    path('transactions-display', views.transactions_display, name="finances.transactions_display"),
    path('profile', views.profile_view, name='finances.profile'),
    path('tickets/<int:ticket_id>/edit', views.edit_ticket, name='finances.edit_ticket'),
    path('tickets/<int:ticket_id>/delete', views.delete_ticket, name='finances.delete_ticket'),
]
