from django.contrib import admin

from .models import Post, Location, Category, Comment


class PostAdmin(admin.ModelAdmin):
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
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published')
    list_editable = ('slug', 'is_published')


admin.site.register(Post, PostAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
