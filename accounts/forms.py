from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import DashboardBackground
from .models import Timetable

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class DashboardBackgroundForm(forms.ModelForm):
    class Meta:
        model = DashboardBackground
        fields = ['image']
class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['image']        