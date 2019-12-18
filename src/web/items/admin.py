from django.contrib import admin
from .models import Item, Profile

class ItemAdmin(admin.ModelAdmin):
    list_filter = ['release_date']
    search_fields = ['title']

class ProfileAdmin(admin.ModelAdmin):
    list_filter = ['username']
    search_fields = ['genre_preferences']

admin.site.register(Item, ItemAdmin)
admin.site.register(Profile, ProfileAdmin)