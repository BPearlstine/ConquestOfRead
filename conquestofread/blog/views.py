import requests
from datetime import datetime

from django.core.files.base import ContentFile
from django.urls import reverse
from django.template.response import TemplateResponse
from django.views.generic import CreateView
from django.views.generic import ListView

from .forms import AddBlogForm
from .models import Blog
from .models import Tag


class Home(ListView):

    model = Blog
    template_name = 'blog/home.html'

    def get_active_episodes(self, curr_date):
        token = 'f79214411501414d1a1412bae3d6303e'
        url = 'https://www.buzzsprout.com/api/288519/episodes.json'
        header = {'Authorization': 'Token token={}'.format(token)}
        r = requests.get(url, headers=header)
        podcasts = r.json()
        print(curr_date)
        active_episodes = [episode for episode in podcasts
                           if datetime.strptime(
                                        episode['published_at'][:episode[
                                                'published_at'].index('T')],
                                        '%Y-%m-%d'
                                        ) <= curr_date]
        for episode in active_episodes:
            tags = episode['tags'].split(',')
            episode['tags'] = tags
            image_content = ContentFile(requests.get(
                                            episode['artwork_url']).content)
            blog, created = Blog.objects.get_or_create(
                            title=episode['title'],
                            pub_date=datetime.strptime(
                                         episode['published_at'][:episode[
                                                 'published_at'].index('T')],
                                         '%Y-%m-%d'),
                            body=episode['description'])
            if created:
                blog.image.save('image.jpg', image_content)
            for tag in tags:
                tag, _ = Tag.objects.get_or_create(tag=tag.strip())
                blog.tags.add(tag)
        return active_episodes

    def get(self, request):
        curr_date = datetime.today()
        self.get_active_episodes(curr_date)
        return TemplateResponse(request, self.template_name)


class AddBlogView(CreateView):
    template_name = 'blog/add_blog.html'
    model = Blog
    form_class = AddBlogForm

    def get_success_url(self):
        return reverse('home')


class BlogsByTagView(ListView):
    template_name = 'blog/tagged.html'
    model = Blog

    def get(self, request, pk):

        self.object_list = self.get_queryset(pk)
        return TemplateResponse(request, self.template_name)

    def get_queryset(self, pk):
        tag = Tag.objects.get(pk=pk)
        blogs = tag.blog_set
        return blogs
