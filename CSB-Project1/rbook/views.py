from django.shortcuts import render, get_object_or_response, redirect
from django.db import connection
from .models import Recipe

def index(request):
    public_recipes = Recipe.objects.filter(secret=False)
    
    my_secret_recipes = []
    if request.user.is_authenticated:
        my_secret_recipes = Recipe.objects.filter(owner=request.user, secret=True)
        
    return render(request, 'rbook/index.html', {
        'public_recipes': public_recipes,
        'my_secret_recipes': my_secret_recipes
    })

# FLAW 1: A01:2025 - Broken Access Control (IDOR)
# VULNERABLE VERSION: Retrieves the recipe directly by ID without checking 
# whether the recipe is secret and whether it belongs to the user making the request.
def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    # FIX:
    # if recipe.secret and recipe.owner != request.user:
    #     raise PermissionDenied("You do not have permission to view this secret recipe.")
    
    return render(request, 'rbook/recipe_detail.html', {'recipe': recipe})

# FLAW 2: A05:2025 - Injection (SQL Injection)
# VULNERABLE VERSION: Using a raw SQL query with string formatting (f-string) 
# instead of an ORM-protected query.
def search(request):
    query = request.GET.get('query', '')
    
    # Vulnerable raw SQL query:
    raw_query = f"SELECT * FROM rbook_recipe WHERE rname LIKE '%{query}%'"
    recipes = Recipe.objects.raw(raw_query)
    
    # FIX:
    # recipes = Recipe.objects.filter(rname__icontains=query)

    return render(request, 'rbook/search_results.html', {
        'query': query,
        'recipes': recipes
    })
