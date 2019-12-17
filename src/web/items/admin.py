from django.contrib import admin
from .models import Item, Consumer

class ItemAdmin(admin.ModelAdmin):
    list_filter = ['release_date']
    search_fields = ['title']

class ConsumerAdmin(admin.ModelAdmin):
    list_filter = ['name']
    search_fields = ['interest']

admin.site.register(Item, ItemAdmin)
admin.site.register(Consumer, ConsumerAdmin)