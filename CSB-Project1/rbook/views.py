from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from .models import Recipe
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, RecipeForm

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

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_dict() if hasattr(form, 'is_dict') else form.is_valid():
            user = form.save()
            login(request, user)  # Login user at the same time
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'rbook/register.html', {'form': form})

# FLAW 4: A02:2025 - Cryptographic Failures / Sensitive Data Exposure
# VULNERABLE VERSION: When creating a secret recipe, the application prints/writes 
# the recipe's "secrets" (e.g. ingredients) directly to the server console/log in plain text,
# and stores them in the database without any protection/encryption.
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.owner = request.user
            recipe.save()
            
            # VULNERABILITY (Flaw 4): Leaking sensitive information to the server log
            if recipe.secret:
                print(f"[SECURITY WARNING LOG] Secret recipe created by {request.user.username}! Secret details: {recipe.ingredients}")

            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'rbook/add_recipe.html', {'form': form})
