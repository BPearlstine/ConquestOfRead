from django.urls import path

from . import views

urlpatterns = [
    path('episodes/',
         views.PodcastListView.as_view(),
         name='podcast_list')
]
