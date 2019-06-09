import requests

from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.detail import View


class PodcastListView(View):
    template_name = 'podcast/podcast_list.html'

    def get(self, request):
        token = 'f79214411501414d1a1412bae3d6303e'
        url = 'https://www.buzzsprout.com/api/288519/episodes.json'
        header = {'Authorization': 'Token token={}'.format(token)}
        r = requests.get(url, headers=header)
        json = r.json()
        context = {'podcast_list': json}
        return TemplateResponse(request, self.template_name, context)
