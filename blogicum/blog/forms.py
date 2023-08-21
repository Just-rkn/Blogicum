from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

from .models import Post, Comment


User = get_user_model()


class PostForm(forms.ModelForm):
    """Form of model Post."""

    class Meta:
        model = Post
        fields = (
            'title', 'text', 'image', 'category', 'location', 'pub_date',
            'is_published'
        )
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):
    """Form of model Comment."""

    class Meta:
        model = Comment
        fields = ('text',)


class UserUpdateForm(UserChangeForm):
    """Modified form of UserChangeForm."""

    password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )
