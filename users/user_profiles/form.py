from django import forms
from django.contrib.auth import authenticate, get_user_model,login,logout
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile

User=get_user_model()

class SignUpForm(forms.Form):
	username = forms.CharField(label="UserName")
	email= forms.EmailField(label="Email", max_length=254, help_text='Requird. Inform a valid email')
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
	password2 = forms.CharField(label="Password (Again)", widget=forms.PasswordInput())

	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
			if password1 == password2:
				return password2
			raise forms.ValidationError('Passwords do not match')

	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		raise forms.ValidationError('Username is already taken.')

class UserLoginForm(forms.Form):
	username = forms.CharField(label="UserName")
	password = forms.CharField(label="Password", widget=forms.PasswordInput)

	def clean(self, *args,**kwargs):
		username= self.cleaned_data.get("username")
		password= self.cleaned_data.get("password")

		
		if username and password:
			user= authenticate(username=username,password=password)
			if not user:
				raise forms.ValidationError("This user does not Exists ")

			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")

			if not user.is_active:
				raise forms.ValidationError("User is no longer active")			

		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        
        #fields = ('first_name', 'last_name', 'email', 'password', 'is_staff', 'username', 'is_superuser')
        fields = ('first_name', 'last_name', 'email')
    widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'name': 'email', 'placeholder': 'email'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        
        fields = ('bio', 'location', 'birth_date', 'profile_photo', 'designation','work_experience', 'education')
    widgets = {
    		'profile_photo': forms.FileInput(attrs={'class':'form-control', 'name':'photo'})
        }
