from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter password"}
        ),
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            raise forms.ValidationError("Username is required.")
        if not password:
            raise forms.ValidationError("Password is required.")

    class Meta:
        model = User
        fields = ('username', 'password')



class UserRegisterForm(UserCreationForm):
    image = forms.ImageField(required=False)
    is_verified_email = forms.BooleanField(required=False)
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter email"}),
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter username..."}
        ),
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter password"}
        ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm password"}
        ),
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password1',
                  'password2', 'image', 'is_verified_email')
        

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'image']

        # class Meta:
        # model = User
        # fields = ['username', 'email', 'first_name', 'last_name', 'image']
        # widgets = {
        #     'username': forms.TextInput(attrs={
        #         'class': "form-control",
        #         'placeholder': 'Username'
        #         }),
        #     'first_name': forms.TextInput(attrs={
        #         'class': "form-control",
        #         'placeholder': 'Username'
        #         }),
        #     'last_name': forms.TextInput(attrs={
        #         'class': "form-control",
        #         'placeholder': 'Username'
        #         }),  
        #     'email': forms.EmailInput(attrs={
        #         'class': "form-control", 
        #         'style': 'max-width: 300px;',
        #         'placeholder': 'Email'
        #         })
        # }
        