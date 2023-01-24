from django.shortcuts import render
from .models import Post, Group, User
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import PostForm

PAGE_RANGE = 10


def paginator_main(arg1, request):
    paginator = Paginator(arg1, PAGE_RANGE)
    page_number = request.GET.get('page')
    pag_get_page = paginator.get_page(page_number)
    return pag_get_page


def index(request):
    post_list = Post.objects.all()
    page_obj = paginator_main(post_list, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    count = author.posts.count()
    page_obj = paginator_main(posts, request)
    context = {
        "page_obj": page_obj,
        "count": count,
        "author": author,
    }

    template = "posts/profile.html"

    return render(request, template, context)


# Создание страницы отдельного поста
def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post, pk=post_id)
    pub_date = post.pub_date
    post_title = post.text[:30]
    author = post.author
    author_posts = author.posts.all()
    context = {
        "post": post,
        "post_title": post_title,
        "author": author,
        "author_posts": author_posts,
        "pub_date": pub_date,
    }

    template = "posts/post_detail.html"

    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = paginator_main(posts, request)
    context = {
        "group": group,
        "page_obj": page_obj,
    }
    return render(request, 'posts/group_list.html', context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(f"/profile/{post.author}/", {"form": form})
    form = PostForm()
    groups = Group.objects.all()
    template = "posts/create_post.html"
    context = {"form": form, "groups": groups}
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    groups = Group.objects.all()
    form = PostForm(request.POST or None, instance=post)
    template = "posts/create_post.html"
    if request.user == author:
        if request.method == "POST" and form.is_valid:
            post = form.save()
            return redirect("posts:post_detail", post_id)
        context = {
            "form": form,
            "is_edit": is_edit,
            "post": post,
            "groups": groups,
        }
        return render(request, template, context)
    return redirect("posts:post_detail", post_id)
