from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import PostForm
from blog.models import Post


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(enabled=True)
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.views += 1
    post.save()
    return render(request, "blog/post_detail.html", {"post": post})


def post_new(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "blog/new_post.html", {"form": form})
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_pk=post.pk)


def post_edit(request, post_pk):
    post = Post.objects.filter(pk=post_pk).first()
    if not post:
        raise Http404("Post not found")
    if request.method == "GET":
        form = PostForm(instance=post)
        return render(request, "blog/post_edit.html", {"form": form})
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', post_pk=post.pk)


def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.delete()
    return redirect("post_list")


def post_like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.like += 1
    post.save()
    return render(request, "blog/post_detail.html", {"post": post})


def post_draft(request):
    posts = Post.objects.filter(enabled=False)
    return render(request, "blog/post_draft.html", {"posts": posts})


def post_public(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.enabled = True
    post.save()
    return render(request, "blog/post_detail.html", {"post": post})
