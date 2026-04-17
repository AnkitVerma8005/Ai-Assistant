from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class EmailSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Use a valid email address.")
    full_name = forms.CharField(max_length=100, required=True, help_text="Required. Enter your full name.")

    class Meta:
        model = User
        fields = ('email', 'full_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={
        'class': 'w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition',
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': 'w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition',
        'placeholder': 'Enter your password'
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise ValidationError("No account found with this email.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()
            if user and not user.is_active:
                raise ValidationError("This account is inactive. Please contact support.")
        
        return cleaned_data
