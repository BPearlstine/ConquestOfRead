from django import forms
from .models import Blog
from .models import Tag

from datetime import date


class AddBlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'body', 'image', 'tags']

    def save(self):
        obj = self.instance
        curr_date = date.today()
        obj.pub_date = curr_date
        obj.save()
