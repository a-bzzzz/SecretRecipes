from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from .models import Recipe
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
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

# FLAW 1: A01:2025 - Broken Access Control 
# (CWE-639: Authorization Bypass Through User-Controlled Key / IDOR)
def recipe_detail(request, recipe_id):
    
    # VULNERABILITY 1: Retrieves the recipe directly by ID without checking 
    # whether the recipe is secret and whether it belongs to the user making the request.
    # recipe = Recipe.objects.get(id=recipe_id) # Does not handle missing recipe
    recipe = get_object_or_404(Recipe, id=recipe_id) # Handles missing recipe with 404, but not user permission
    
    # FIX 1: Restrict secret recipes to owner only.
    # recipe = get_object_or_404(Recipe, id=recipe_id)
    # if recipe.secret and recipe.owner != request.user:
    #     raise PermissionDenied("You do not have permission to view this secret recipe.")
    
    return render(request, 'rbook/recipe_detail.html', {'recipe': recipe})

# FLAW 2: A05:2025 - Injection 
# (CWE-89: SQL Injection)
def search(request):
    query = request.GET.get('query', '')
    
    # VULNERABILITY 2: Using a raw SQL query with string formatting (f-string) 
    # instead of an ORM-protected query.
    raw_query = f"SELECT * FROM rbook_recipe WHERE rname LIKE '%{query}%'"
    recipes = Recipe.objects.raw(raw_query)
    
    # FIX 2: Use Django's ORM parametrized query.
    # recipes = Recipe.objects.filter(rname__icontains=query, secret=False)

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

# FLAW 4: A09:2025 Security Logging and Alerting Failures 
# (CWE-532: Insertion of Sensitive Information into Log File)
@login_required
def add_recipe(request):
    
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.owner = request.user
            recipe.save()
            
            # VULNERABILITY 4: Leaking sensitive information to the server log.
            # When creating a secret recipe, the application prints/writes 
            # the recipe's "secrets" (e.g. ingredients) directly to the server console/log in plain text,
            # and stores them in the database without any protection/encryption.
            if recipe.secret:
                print(f"[SECURITY WARNING LOG] Secret recipe created by {request.user.username}! Secret details: {recipe.ingredients}")
        
            # FIX 4: Remove sensitive data logging or mask sensitive values.
            # if recipe.secret:
            #     print(f"[SECURITY WARNING LOG] Secret recipe ID {recipe.id} created by user {request.user.id}") 

            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'rbook/add_recipe.html', {'form': form})
