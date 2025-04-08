from django.contrib import admin
from .models import Transaction, Income

admin.site.register(Income)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'type', 'date')
    list_filter = ('category', 'type', 'date')
    search_fields = ('category', 'with_who_or_what')
