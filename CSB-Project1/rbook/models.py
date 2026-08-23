from django.db import models
from django.contrib.auth.models import User

# Recipe categories for drop-down list
CATEGORY_CHOICES = [
	('breakfast', 'Breakfast'),
	('first_dish', 'Appetizers'),
	('soup', 'Soups'),
	('salad', 'Salads'),
	('main_dish', 'Main Dishes'),
	('side_dish', 'Side Dishes'),
	('dessert', 'Desserts'),
	('drink', 'Drinks'),
	('bake', 'Baking'),
]

class Recipe(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')

	category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='main_dish')
    secret = models.BooleanField(default=False)
    portions = models.IntegerField(default=1)
	
	# Simplified input feed with a new line, eg.
    # - 3 dl milk
    # - 2 tbsp cocoa powder
    ingredients = models.TextField(help_text="Enter each amount & ingredient on a new line")
    guidance = models.TextField(help_text="Enter preparation steps on new lines")

def __str__(self):
        return self.rname
