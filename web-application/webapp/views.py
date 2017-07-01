from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from main.parameters import Messages
from webapp import forms
from webapp.models import Post, Category, Status


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


class PostAddView(CreateView):
    success_message = Messages.Post.adding_success
    template_name = 'post_add.html'
    model = Post
    form_class = forms.PostForm

    def get(self, request):
        if self.request.user.is_authenticated():
            return render(request, self.template_name, {'form': self.form_class})
        return HttpResponseRedirect(request.GET.get('next', reverse('home')))

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.status = Status.objects.get(name='На модерации')
        post.save()
        return super(PostAddView, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return reverse('home')

