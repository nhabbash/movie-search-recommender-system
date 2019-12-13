import os, sys
sys.path.append('/code/main')
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

import django
django.setup()

from items.search import search

items = search('Subdue')


print(items)
print(items[0].overview)