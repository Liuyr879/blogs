from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment, Category, Favorites
from blog.forms import PostForm
from django.http import Http404


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(enabled=True)
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = Comment.objects.filter(post=post_pk)
    post.views += 1
    post.save()
    return render(request, "blog/post_detail.html", {"post": post,
                                                     "comments": comments})


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


def category_list(request):
    categorys = Category.objects.all()
    return render(request, "blog/category_list.html", {'categorys': categorys})


def category_in_list(request, category_id):
    posts = Post.objects.filter(category=category_id)
    return render(request, "blog/post_list.html", {'posts': posts})


def post_select(request, post_pk):
    user = request.user
    post = get_object_or_404(Post, pk=post_pk)
    if not Favorites.objects.filter(user=user, post=post).first():  
        Favorites.objects.create(user=user, post=post)
    return render(request, "blog/post_detail.html", {"post": post})


def post_favorites(request):
    posts = [i.post for i in Favorites.objects.filter(user=request.user)]
    return render(request, "blog/post_list.html", {"posts": posts})