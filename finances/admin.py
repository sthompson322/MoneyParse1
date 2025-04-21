from django.contrib import admin
from .models import Transaction, Income, Budget, Ticket

admin.site.register(Income)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'type', 'date')
    list_filter = ('category', 'type', 'date')
    search_fields = ('category', 'with_who_or_what')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'limit')
    list_filter = ('category', 'limit')
    search_fields = ('category', 'limit')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('subject', 'message', 'user__username')
