import os, sys
sys.path.append('/code/main')
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

import django
django.setup()

## End setup

from items.models import Item, Profile
from django.contrib.auth import get_user_model

print("Creating root user if it doesn't exist...")

User = get_user_model()
User.objects.filter(username='root').exists() or \
    User.objects.create_superuser('root', 'root@example.com', 'root')
print(">Done")

Item.populate()
Profile.populate()
