from items.models import Item
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','main.settings')
django.setup()
Item.populate()