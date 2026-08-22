from django.shortcuts import render

@login_required
def addView(request):

	if request.method == 'POST':
		new_recipe = request.POST.get('recipes')
		user = request.user

		if new_recipe:
			Recipes.objects.create(id=id, rname=rname, category=category, secret=secret, portions=portions, ingredients=ingredients, guidance=guidance)

		return redirect('/')

	return redirect('/')

@login_required
def homePageView(request):
	items = request.session.get('recipes', [])		

	return render(request, 'templates/index.html', {'recipes' : recipes})
