from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm
)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
#from captcha.fields import CaptchaField


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    captcha_input = forms.CharField(max_length=6, label='Código de verificación')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']

# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(
#         label=_("Email"),
#         max_length=254,
#         widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
#     )
#     captcha = CaptchaField()

    
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('username', 'email')
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['password1'].widget.attrs.update({'class': 'form-control'})
#         self.fields['password2'].widget.attrs.update({'class': 'form-control'}) 



class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'bio', 'role', 'github_profile']

        


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Email or Username"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label=_("Remember me")
    )