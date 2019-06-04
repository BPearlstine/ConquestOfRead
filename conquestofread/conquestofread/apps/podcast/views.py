import requests

from django.conf import settings
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.detail import View
# Create your views here.


class PodcastListView(View):
    template_name = 'podcast_list.html'

    def get(self, request):
        token = settings.buzzsprout_token
        url = 'https://www.buzzsprout.com/api/288519/episodes.json'
        header = {'Authorization': 'Token token={}'.format(token)}
        r = requests.get(url, headers=header)
        json = r.json()
        context = {'podcast_list': json}
        return TemplateResponse(request, self.template_name, context)
