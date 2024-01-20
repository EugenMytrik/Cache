from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import BlogForm
from .models import Blog


def base_page(request):
    blogs = Blog.objects.all()

    if request.method == "GET":
        return render(request, "base_page.html", {"blogs": blogs})

    if "redirect_on_blog" in request.POST:
        blog_id = request.POST.get("redirect_on_blog")
        return redirect(reverse("blog_page", args={blog_id}))


def blog_page(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    cached_blog = cache.get(f"blog{blog_id}")

    if not cached_blog or cached_blog.updated_at != blog.updated_at:
        cache.set(f"blog{blog_id}", blog, 60 * 15)
    else:
        blog = cached_blog

    if request.method == "GET":
        return render(request, "blog_page.html", {"blog": blog})

    if "edit_blog" in request.POST:
        blog_id = request.POST.get("edit_blog")
        return redirect(reverse("edit_blog", args={blog_id}))

    if "all_blogs" in request.POST:
        return redirect("base_page")


def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    cached_blog = cache.get(f"blog{blog_id}")

    if not cached_blog or cached_blog.updated_at != blog.updated_at:
        cache.set(f"blog{blog_id}", blog, 60 * 15)
    else:
        blog = cached_blog

    if request.method == "GET":
        form = BlogForm(instance=blog)
        return render(request, "edit_page.html", {"form": form})
    form = BlogForm(request.POST, instance=blog)

    if form.is_valid() and "save_blog" in request.POST:
        form.save()
        return redirect(reverse("blog_page", args={blog.id}))
