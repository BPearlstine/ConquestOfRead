from django.urls import path
from . import views

urlpatterns = [
     path('new-post',
          views.AddBlogView.as_view(),
          name='add_blog'),

     path('blogs-by-tag/<int:pk>/',
          views.BlogsByTagView.as_view(),
          name='blogs_by_tag'),

     path('blog-detail/<int:pk>/',
          views.BlogDetailView.as_view(),
          name='detail'),

     path('delete-blog/<int:pk>/',
          views.DeleteBlogView.as_view(),
          name='delete')
]
