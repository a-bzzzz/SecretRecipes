from django import forms
from django.contrib.auth.models import User
from .models import Recipe
from django.contrib.auth.password_validation import validate_password

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    # FLAW 3: A07:2025 - Authentication Failures (CWE-521: Weak Password Requirements)    
    def save(self, commit=True):
        user = super().save(commit=False)
        raw_password = self.cleaned_data["password"]

        # VULNERABILITY 3: Bypass Django's password checks (validate_password)
        # and store the password directly without any strength requirements.
        user.set_password(self.cleaned_data["password"])

        # FIX 3: Enforce standard Django password validation
        # validate_password(raw_password, user)
        
        user.set_password(raw_password)
        
        if commit:
            user.save()
        return user

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['rname', 'category', 'portions', 'ingredients', 'guidance', 'secret']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 4}),
            'guidance': forms.Textarea(attrs={'rows': 4}),
        }
