import requests

from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.detail import View

class Home(View):
    template_name = 'podcast/home.html'

    def get(self, request):
        blogs = Blog.objects.all()
        context = {'blogs': blogs}
        return TemplateResponse(request, self.template_name, context)
