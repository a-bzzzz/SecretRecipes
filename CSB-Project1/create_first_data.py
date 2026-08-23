import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secret_recipes.settings')
django.setup()

from django.contrib.auth.models import User
from recipes.models import Recipe

# Create first users
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'coffee')

if not User.objects.filter(username='bob').exists():
    User.objects.create_user('bob', 'bob@example.com', 'passwd')

# Create first recipe
bob = User.objects.get(username='bob')
if not Recipe.objects.filter(rname='Hot Chocolate').exists():
    Recipe.objects.create(
        owner=bob,
        rname='Hot Chocolate',
        category='drinks',
        secret=True,
        portions=2,
        ingredients="3 dl milk\n2 tbsp cocoa powder\n2 tbsp sugar",
        guidance="1. Heat milk in a pot.\n2. Whisk cocoa and sugar into milk.\n3. Pour into two mugs and serve."
    )

print("Test data created successfully!")
