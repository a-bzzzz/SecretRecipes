from django import forms
from django.contrib.auth.models import User
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm

# FLAW 3: A07:2025 - Authentication Failures 
# (CWE-521: Weak Password Requirements)
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    # VULNERABILITY 3: Saves password without any length or complexity checks
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
        return user
        
# FIX 3: Use Django's built-in UserCreationForm, 
# which enforces strong password validation policies (CWE-521).
# class RegisterForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         fields = ("username",)
        

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['rname', 'category', 'portions', 'ingredients', 'guidance', 'secret']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 4}),
            'guidance': forms.Textarea(attrs={'rows': 4}),
        }
