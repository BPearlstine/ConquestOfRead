import requests
from datetime import datetime

from django.shortcuts import reverse
from django.template.response import TemplateResponse
from django.views.generic.detail import View
from django.views.generic.edit import CreateView

from .forms import AddBlogForm
from .models import Blog


class Home(View):
    template_name = 'blog/home.html'

    def get_active_episodes(self, curr_date):
        token = 'f79214411501414d1a1412bae3d6303e'
        url = 'https://www.buzzsprout.com/api/288519/episodes.json'
        header = {'Authorization': 'Token token={}'.format(token)}
        r = requests.get(url, headers=header)
        podcasts = r.json()
        active_episodes = [episode for episode in podcasts
                           if datetime.strptime(
                                        episode['published_at'][:9],
                                        '%Y-%m-%d'
                                        ) <= curr_date]
        return active_episodes

    def build_post_list(self):
        curr_date = datetime.today()
        blogs = Blog.objects.all()
        active_episodes = self.get_active_episodes(curr_date)
        blog_len = len(blogs)
        cast_len = len(active_episodes)

        post_list = []
        i = 0
        j = 0

        while i < blog_len and j < cast_len:
            if (blogs[i].pub_date.replace(tzinfo=None) >
                datetime.strptime(active_episodes[j]['published_at'][:9],
                                  '%Y-%m-%d')):
                post_list.append([blogs[i], 'blog'])
                i += 1

            else:
                post_list.append([active_episodes[j], 'podcast'])
                j += 1

        while i < blog_len:
            post_list.append([blogs[i], 'blog'])
            i += 1
        while j < cast_len:
            post_list.append([active_episodes[j], 'podcast'])
            j += 1

        return post_list

    def get(self, request):
        post_list = self.build_post_list()
        context = {'post_list': post_list}
        return TemplateResponse(request, self.template_name, context)


class AddBlogView(CreateView):
    template_name = 'blog/add_blog.html'
    model = Blog
    form_class = AddBlogForm

    def get_success_url(self):
        return reverse('home')
