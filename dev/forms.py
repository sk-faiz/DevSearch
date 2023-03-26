from django.forms import ModelForm
from .models import Post, Review
from django import forms


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'featured_image', 'description',
                  'tags', 'demo_link', 'source_link']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input'
            })

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        # widgets = {
        #     'value': forms.RadioSelect(),
        # }
        labels = {
            'value': 'Place your vote',
            'body': 'Write your review'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input'
            })