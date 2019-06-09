from django.urls import path
from . import views

urlpatterns = [
    path('new-post',
         views.AddBlogView.as_view(),
         name='add_blog')
]
