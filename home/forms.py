from django import forms
from django.contrib.auth.forms import UserCreationForm
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