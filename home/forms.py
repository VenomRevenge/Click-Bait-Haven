from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

user = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = user
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        # remove all help texts for now
        for field_name in list(self.fields):
            if field_name not in self.Meta.fields:
                self.fields.pop(field_name)
            else:
                self.fields[field_name].help_text = None
                self.fields[field_name].widget.attrs.pop('placeholder', None)


class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Username or Email'
        for field_name in self.fields:
            self.fields[field_name].help_text = None
