from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

import datetime as dt


User = get_user_model()

MAX_WORDS_PER_STR = 3


class PostManager(models.Manager):
    """Custom Manager of model Post to add extra method."""

    def get_published(self):
        """
        Returns QuerySet of model Post where:
        post pub_date equal to now or earlier
        post is published
        post category is published.
        """

        return self.select_related(
            'author', 'location', 'category'
        ).filter(
            pub_date__lte=dt.datetime.now(tz=timezone.utc),
            is_published=True,
            category__is_published=True
        )


class CreatedAtModel(models.Model):
    """Abstract class that adds published and creation date."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True


class Category(CreatedAtModel):
    """Stores a single category."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        title_words = self.title.split()
        if len(title_words) > MAX_WORDS_PER_STR:
            return f'({self.id}) {" ".join(title_words[:MAX_WORDS_PER_STR])}'
        return f'({self.id}) {self.title}'


class Location(CreatedAtModel):
    """Stores a single location."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        name_words = self.name.split()
        if len(name_words) > MAX_WORDS_PER_STR:
            return f'({self.id}) {" ".join(name_words[:MAX_WORDS_PER_STR])}'
        return f'({self.id}) {self.name}'


class Post(CreatedAtModel):
    """
    Stores a single post, related to :model:'auth.User',
    :model:'blog.Location' and :model:'blog.Category'.
    """

    objects = PostManager()
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем '
            '— можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение',
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts'
    )
    image = models.ImageField(
        verbose_name='Фото', upload_to='posts_images/', blank=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        title_words = self.title.split()
        if len(title_words) > MAX_WORDS_PER_STR:
            return f'({self.id}) {" ".join(title_words[:MAX_WORDS_PER_STR])}'
        return f'({self.id}) {self.title}'


class Comment(models.Model):
    """
    Stores a single comment, related to :model:'blog.Post' and
    :model:'auth.User'.
    """

    text = models.TextField(verbose_name='Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ('created_at',)

    def __str__(self):
        text_words = self.text.split()
        if len(text_words) > MAX_WORDS_PER_STR:
            return f'({self.id}) {" ".join(text_words[:MAX_WORDS_PER_STR])}'
        return f'({self.id}) {self.text}'
