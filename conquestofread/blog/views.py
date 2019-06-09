import requests

from django.shortcuts import render
from django.shortcuts import reverse
from django.template.response import TemplateResponse
from django.views.generic.detail import View
from django.views.generic.edit import CreateView

from .forms import AddBlogForm
from .models import Blog

class Home(View):
    template_name = 'blog/home.html'

    def get(self, request):
        blogs = Blog.objects.all()
        context = {'blogs': blogs}
        return TemplateResponse(request, self.template_name, context)

class AddBlogView(CreateView):
    template_name = 'blog/add_blog.html'
    model = Blog
    form_class = AddBlogForm

    def get_success_url(self):
        return reverse('home')
