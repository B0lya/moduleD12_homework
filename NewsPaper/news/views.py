from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from django.core.paginator import Paginator
from .filters import NewsFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.core.cache import cache

from django.shortcuts import HttpResponseRedirect




class NewsList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

class NewsDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"

    def subscribe(request, pk):
        user = request.user
        category = Category.objects.get(pk=pk)
        if user not in category.subscribers.all():
            category.subscribers.add(user)
        else:
            category.subscribers.remove(user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'news_create.html'
    form_class = PostForm
    success_url = '/news'

   

class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'news_create.html'
    form_class = PostForm
    success_url = '/news'

    
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news'

    
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    

    

