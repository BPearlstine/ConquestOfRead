from django import forms
from .models import Blog
from .models import Tag

from datetime import date


class AddBlogForm(forms.ModelForm):

    tag = forms.CharField()
    image = forms.ImageField(required=False)

    class Meta:
        model = Blog
        fields = ['title', 'body', 'image', 'tag']
        help_texts = {'tag': 'Enter tags seperated by commas'}

    def save(self):
        obj = self.instance
        data = self.cleaned_data
        curr_date = date.today()
        obj.pub_date = curr_date
        tags = data['tag']
        tags = [tag for tag in tags.split(',')]
        obj.save()
        for tag in tags:
            tag_model, _ = Tag.objects.get_or_create(tag=tag)
            obj.tags.add(tag_model)
        obj.save()
