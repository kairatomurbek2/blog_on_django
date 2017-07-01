from django import forms
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from redactor.widgets import RedactorEditor

from webapp.models import Category, Post, Status


class CategoryAdmin(DraggableMPTTAdmin):
    list_filter = ['is_active']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'slug']


class PostAdminForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'info': RedactorEditor()
        }


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at', 'status']
    list_filter = ['created_at', 'category', 'status']
    search_fields = ['title', 'slug']
    prepopulated_fields = {"slug": ("title",)}
    form = PostAdminForm


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Status)
