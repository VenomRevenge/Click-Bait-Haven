from django import forms
from articles.models import Article, Comment, Tag

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
                'placeholder': 'Write your article here...(minimum 500 characters)',
                'cols': 40,
                'rows': 40,
                'minlength': Article.CONTENT_MIN_LENGTH,
                }
            ),
        }


class ArticleEditForm(ArticleCreateForm):

    class Meta(ArticleCreateForm.Meta):
        labels = {
            'picture': 'Change cover picture',
            'title': 'Edit title',
            'content': 'Edit content',
            'tags': 'Edit tags',
        }


class ArticleSearchForm(forms.Form):

    title = forms.CharField(
        label="Search by title",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Article title..."})
    )
    username = forms.CharField(
        label="From author",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Author's username..."})
    )
    order_by = forms.ChoiceField(
        label="Sort by",
        required=False,
        choices=[
            ("-created_at", "Date (Newest)"),
            ("created_at", "Date (Oldest)"),
        ],
        widget=forms.Select()
    )
    tag = forms.MultipleChoiceField(
        label="Tags",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]  
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tag'].choices = [(tag.name, tag.name) for tag in Tag.objects.all().order_by('name')]


class CommentEditForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = ['content']

        labels = {
            'content': 'Comment',
        }