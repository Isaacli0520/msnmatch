from django.contrib import admin
from .models import Item

class CustomItemAdmin(admin.ModelAdmin):
    list_display = ['name','category', 'condition', 'price', 'sold', 'pickup','delivery']
    list_filter = ('category', 'condition', 'sold', 'pickup','delivery')


admin.site.register(Item, CustomItemAdmin)