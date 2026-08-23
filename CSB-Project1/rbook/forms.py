from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    # FLAW 3: A07:2025 - Identification and Authentication Failures
    # VULNERABLE VERSION: Bypass Django's password checks (validate_password)
    # and store the password directly without any strength requirements.
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
