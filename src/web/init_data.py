import os, sys
sys.path.append('/code/main')
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

import django
django.setup()

from items.models import Item

if sys.argv[1] == "clear":
    print("Deleting...")
    Item.objects.all().delete()
elif sys.argv[1] == "populate":
    print("Populating...")
    Item.populate()
