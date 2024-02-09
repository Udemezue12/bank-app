from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'membership', 'birth_date', 'country', 'state']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']