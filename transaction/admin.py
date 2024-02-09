from django.contrib import admin
from . import models

# Register your models here.


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'previous_balance', 'current_balance', 'amount', 'transaction_id']

admin.site.register(models.Transaction, TransactionAdmin)
