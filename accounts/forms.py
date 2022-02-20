from django import forms

from .models import User
from django.contrib.auth.forms import AuthenticationForm


class UserRegisterationForm(forms.ModelForm):
    user_name = forms.CharField(label='Enter Username', min_length=4, max_length=50,
                                help_text='Required', widget=forms.TextInput(attrs={'class': 'form-control mb-3',
                                                                                    'placeholder': 'Username'}
                                                                             ))
    email = forms.EmailField(label='Enter Your email', help_text='Required',
                             error_messages={'required': 'Sorry, you will need an email'}, widget=forms.EmailInput(attrs={'class': 'form-control mb-3', 'placeholder': 'E-mail',
                                                                                                                          'name': 'email', 'id': 'id_email'}
                                                                                                                   ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'Enter your password'
    }))
    password2 = forms.CharField(
        label='Confirm your password', widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Enter your password confirmation'
        }))

    class Meta:
        model = User
        fields = ('user_name', 'email')

    # def clean_user_name(self):
    #     print('clean_username has been callled 🌹🌹🌹🌹🌹')
    #     user_name = self.cleaned_data['user_name'].lower()
    #     r = User.objects.filter(user_name=user_name)
    #     if r.count():
    #         raise forms.ValidationError(
    #             'Username already exists bla bla bla')
    #     return user_name

    def clean_password2(self):
        print('clean_password2 has been callled 🌹🌹🌹🌹🌹')
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not match bla bla bla ')
        return self.cleaned_data['password2']

    def clean_email(self):
        print('clean_email has been callled 🌹🌹🌹🌹🌹')
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'This email address has been already used bla bla bla')
        return email

    # def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        # self.fields['user_name'].widget.attrs.update(
        #     {'class': 'form-control mb-3', 'placeholder': 'Username'})
        # self.fields['email'].widget.attrs.update(
        #     {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        # self.fields['password'].widget.attrs.update(
        #     {'class': 'form-control mb-3', 'placeholder': 'Password'})
        # self.fields['password2'].widget.attrs.update(
        #     {'class': 'form-control', 'placeholder': 'Repeat Password'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3', 'placeholder': 'Enter your email', 'id': 'login-username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password', 'id': 'login-pwd'
    }))


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-lastname'}))

    class Meta:
        model = User
        fields = ('email', 'first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True
