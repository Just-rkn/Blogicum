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

POSTS_PER_PAGE = 10


class CommentMixin:
    """
    Mixin that adds model, form_class, template_name and
    modifying method get_success_url.
    """

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_success_url(self):
        """
        Determine the URL to redirect to the correct post when the
        CommentForm is successfully processed.
        """

        return reverse(
            'blog:post_detail', kwargs={'post_pk': self.kwargs['post_pk']}
        )


class CommentDispatchMixin:
    """
    Mixin that adds pk_url_kwarg and
    modifying method dispatch.
    """

    pk_url_kwarg = 'comment_pk'

    def dispatch(self, request, *args, **kwargs):
        """
        Gets the correct comment or raise 404 error,
        if the comment does not exist.
        If comment author is not equal to the request user,
        redirect to the post page.
        """

        comment = get_object_or_404(Comment, pk=kwargs['comment_pk'])
        if comment.author != request.user:
            return redirect(
                'blog:post_detail', post_pk=kwargs['post_pk']
            )
        return super().dispatch(request, *args, **kwargs)


class PostDispatchMixin:
    """
    Mixin that adds model, form_class, template_name,
    pk_url_kwarg and modifying method dispatch.
    """

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_pk'

    def dispatch(self, request, *args, **kwargs):
        """
        Gets the correct post or raise 404 error,
        if the post does not exist
        if post author is not equal to the request user,
        redirect to the post page.
        """

        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        if post.author != self.request.user:
            return redirect('blog:post_detail', post_pk=kwargs['post_pk'])
        return super().dispatch(request, *args, **kwargs)


class PaginateMixin:
    """Mixin that adds model and paginate_by"""

    model = Post
    paginate_by = POSTS_PER_PAGE


class HomepageListView(PaginateMixin, ListView):
    """CBV that displays posts on 'index.html'."""

    template_name = 'blog/index.html'
    queryset = Post.objects.get_published()


class CategoryListView(PaginateMixin, ListView):
    """
    CBV that displays posts of a specific category on 'category.html'.
    """

    template_name = 'blog/category.html'

    def get_queryset(self):
        """
        Returns the QuerySet of the correct category,
        if there is no correct category or category is not published,
        raise 404 error.
        """

        category = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True
        )
        queryset = Post.objects.get_published().filter(
            category=category
        )
        return queryset

    def get_context_data(self, **kwargs):
        """Adds information about the category to the context."""

        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, slug=self.kwargs['category_slug']
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    CBV that displays UserUpdateForm with user instance on 'user.html'.
    """

    model = User
    form_class = UserUpdateForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        """Returns the username from the request."""

        return User.objects.get(username=self.request.user)

    def get_success_url(self):
        """
        Determine the URL to redirect to the correct user profile
        when the UserUpdateForm is successfully processed.
        """

        return reverse('blog:profile', kwargs={'username': self.request.user})


class ProfileListView(PaginateMixin, ListView):
    """
    CBV that displays posts of a specific author on 'profile.html'.
    """

    template_name = 'blog/profile.html'

    def get_queryset(self):
        """
        Returns the QuerySet of the correct author,
        if there is no correct author,
        raise 404 error.
        """

        author = get_object_or_404(User, username=self.kwargs['username'])
        queryset = Post.objects.select_related(
            'author', 'category', 'location'
        ).filter(
            author=author
        )
        return queryset

    def get_context_data(self, **kwargs):
        """Adds information about the user to the context."""

        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    CBV that displays PostForm on 'create.html'.
    """

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        """Adds the author to the form."""

        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Determine the URL to redirect to the correct user profile
        when the UserCreateForm is successfully processed.
        """

        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostDetailView(DetailView):
    """
    CBV that displays correct post on 'detail.html'.
    """

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_pk'

    def dispatch(self, request, *args, **kwargs):
        """
        Gets the correct post or raise 404 error,
        if the post does not exist.
        If post author is not equal to the request user and
        post is not published raise 404 error.
        """

        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        if post.is_published is False and request.user != post.author:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Adds the CommentForm and post comments to the context."""

        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostUpdateView(PostDispatchMixin, LoginRequiredMixin, UpdateView):
    """
    CBV that displays PostForm with post instance on 'create.html'.
    """

    def get_success_url(self):
        """
        Determine the URL to redirect to the correct post
        when the PostForm is successfully processed.
        """

        return reverse(
            'blog:post_detail', kwargs={'post_pk': self.kwargs['post_pk']}
        )


class PostDeleteView(PostDispatchMixin, LoginRequiredMixin, DeleteView):
    """CBV that displays post information on 'create.html'."""

    def get_context_data(self, **kwargs):
        """Adds the PostForm with instance to the context."""

        context = super().get_context_data(**kwargs)
        instance = Post.objects.get(pk=self.kwargs['post_pk'])
        context['form'] = PostForm(instance=instance)
        return context

    def get_success_url(self):
        """
        Determine the URL to redirect to the correct user profile
        when the PostForm is successfully processed.
        """

        return reverse('blog:profile', kwargs={'username': self.request.user})


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    """
    CBV that displays CommentForm on 'comment.html'.
    """

    def form_valid(self, form):
        """Adds the author and post to the form."""

        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)


class CommentDeleteView(
    CommentMixin, CommentDispatchMixin, LoginRequiredMixin, DeleteView
):
    """CBV that displays comment information on 'comment.html'."""
    pass


class CommentUpdateView(
    CommentMixin, CommentDispatchMixin, LoginRequiredMixin, UpdateView
):
    """
    CBV that displays CommentForm with comment instance on 'comment.html'.
    """
    pass
