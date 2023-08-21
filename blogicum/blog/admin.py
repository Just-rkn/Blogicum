from django.contrib import admin

from .models import Post, Location, Category, Comment


class PostAdmin(admin.ModelAdmin):
    """
    ModelAdmin of model Post.

    Attributes
    ----------
    list_display: tuple
        fields that are displayed on the change list page of the admin

    list_editable: tuple
        fields that are allowed to be edited on
        the changelist page of the admin

    search_fields: tuple
        fields that will be searched whenever somebody submits a search
        query in text box on the admin change list page,
        these fields should be some kind of text field

    list_filter: tuple
        fields that can be filtered by in the right sidebar of
        the change list page in the admin

    """

    list_display = (
        'title',
        'pub_date',
        'is_published',
        'author',
        'category',
        'location'
    )
    list_editable = (
        'pub_date',
        'is_published'
    )
    search_fields = ('title',)
    list_filter = ('author', 'category', 'location')


class LocationAdmin(admin.ModelAdmin):
    """
    ModelAdmin of model Location.

    Attributes
    ----------
    list_display: tuple
        fields that are displayed on the change list page of the admin

    list_editable: tuple
        fields that are allowed to be edited on
        the changelist page of the admin

    search_fields: tuple
        fields that will be searched whenever somebody submits a search
        query in text box on the admin change list page,
        these fields should be some kind of text field

    """

    list_display = ('name', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    """
    ModelAdmin of model Category.

    Attributes
    ----------
    list_display: tuple
        fields that are displayed on the change list page of the admin

    list_editable: tuple
        fields that are allowed to be edited on
        the changelist page of the admin

    """

    list_display = ('title', 'slug', 'is_published')
    list_editable = ('slug', 'is_published')


admin.site.register(Post, PostAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
