from django import forms
from profiles.models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = (
            'profile_picture',
            'bio',
            'gender',
            'date_of_birth',
        )

        labels = {
            'profile_picture': 'Profile Picture',
            'date_of_birth': 'Date of Birth',
        }

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type something about yourself...'}),
        }