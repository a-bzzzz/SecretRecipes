from django.db import models

from django.contrib.auth.models import User, Recipes

class Recipe(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	recipe = models.TextField()
