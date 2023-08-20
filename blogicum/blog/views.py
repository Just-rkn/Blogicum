from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import Http404
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView
)

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, UserUpdateForm


User = get_user_model()


class CommentMixin:
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_pk': self.kwargs['post_pk']}
        )


class CommentDispatchMixin:
    pk_url_kwarg = 'comment_pk'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['comment_pk'])
        if comment.author != request.user:
            return redirect(
                'blog:post_detail', post_pk=kwargs['post_pk']
            )
        return super().dispatch(request, *args, **kwargs)


class PostDispatchMixin:
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_pk'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        if post.author != self.request.user:
            return redirect('blog:post_detail', post_pk=kwargs['post_pk'])
        return super().dispatch(request, *args, **kwargs)


class PaginateMixin:
    model = Post
    paginate_by = 10


class HomepageListView(PaginateMixin, ListView):
    template_name = 'blog/index.html'
    queryset = Post.objects.get_published()


class CategoryListView(PaginateMixin, ListView):
    template_name = 'blog/category.html'

    def get_queryset(self):
        category = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True
        )
        queryset = Post.objects.get_published().filter(
            category=category
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, slug=self.kwargs['category_slug']
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return User.objects.get(username=self.request.user)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class ProfileListView(PaginateMixin, ListView):
    template_name = 'blog/profile.html'

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        queryset = Post.objects.select_related(
            'author', 'category', 'location'
        ).filter(
            author=author
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_pk'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        if post.is_published is False and request.user != post.author:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostUpdateView(PostDispatchMixin, LoginRequiredMixin, UpdateView):

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_pk': self.kwargs['post_pk']}
        )


class PostDeleteView(PostDispatchMixin, LoginRequiredMixin, DeleteView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = Post.objects.get(pk=self.kwargs['post_pk'])
        context['form'] = PostForm(instance=instance)
        return context

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)


class CommentDeleteView(
    CommentMixin, CommentDispatchMixin, LoginRequiredMixin, DeleteView
):
    pass


class CommentUpdateView(
    CommentMixin, CommentDispatchMixin, LoginRequiredMixin, UpdateView
):
    pass
