from django.forms import ModelForm
from .models import Article, Review
from django import forms


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['body', 'value']

        labels = {
            'body': 'Add a comment to your vote',
            'value': 'Place your vote'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'featured_image', 'description', 'tags']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
