from blog.views import post_delete, post_detail, post_draft, post_edit, post_like, post_list, post_new, post_public
from django.urls import include, path

urlpatterns = [
    path('list/', post_list, name="post_list"),
    path('detail/<int:post_pk>', post_like, name="post_like"),
    path('detail/<int:post_pk>/', post_detail, name="post_detail"),
    path('new/', post_new, name="post_new"),
    path('edit/<int:post_pk>/', post_edit, name="post_edit"),
    path('delete/<int:post_pk>/', post_delete, name="post_delete"),
    path('draft/', post_draft, name="post_draft"),
    path('Publish a post/<int:post_pk>/', post_public, name="post_public"),
]
