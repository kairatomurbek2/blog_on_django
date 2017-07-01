from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView
from webapp.models import Post, Category


class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'posts'
    paginate_by = 30

    def get_queryset(self):
        posts = Post.objects.all().order_by('-created_at')
        return posts


class CategoriesView(ListView):
    template_name = 'category_post.html'
    model = Category
    paginate_by = 30

    def get_queryset(self):
        queryset = super(CategoriesView, self).get_queryset()
        return queryset.filter(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(CategoriesView, self).get_context_data(**kwargs)
        posts = Post.objects.filter(category__slug=self.kwargs['slug'])
        paginator = Paginator(posts, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts_category'] = posts
        return context


class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    model = Post

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs['post_slug'], status__name='Активный')
