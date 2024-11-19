from django import forms
from articles.models import Article, Tag

class ArticleCreateForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Article

        fields = [
            'picture',
            'title',
            'content',
            'tags',
        ]

        labels = {
            'picture': 'Upload a Cover Picture',
        }

        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your article here...',
                'cols': 40,
                'rows': 40,
                }
            ),
        }