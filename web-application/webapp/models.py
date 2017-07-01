from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from redactor.fields import RedactorField
from main.media_path import blog_image_upload_path


class Status(models.Model):
    name = models.CharField(verbose_name=_('Название'), max_length=80)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Статус')
        verbose_name_plural = _('Статусы')


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super(CategoryManager, self).get_queryset().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(verbose_name=_('Название'), max_length=80)
    slug = models.SlugField(verbose_name=_('Ярлык'), max_length=90, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    is_active = models.BooleanField(verbose_name=_('Активна'), default=True)
    all_objects = models.Manager()
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_list', kwargs={'slug': self.slug})

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')


class PostManager(models.Manager):
    def get_queryset(self):
        return super(PostManager, self).get_queryset().filter(status__name='Активный')


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts')
    title = models.CharField(max_length=100, verbose_name=_('Название'))
    slug = models.SlugField(verbose_name=_('Ссылка'))
    image = models.ImageField(verbose_name=_('Изображение'), upload_to=blog_image_upload_path, blank=True)
    info = RedactorField(verbose_name=_('информация'))
    category = models.ForeignKey(Category, related_name='category_blogs', verbose_name=_('Категории'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    status = models.ForeignKey(Status, related_name='statuses', verbose_name=_('Статус'), blank=True, null=True)
    all_objects = models.Manager()
    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.category.slug, 'post_slug': self.slug})

    class Meta:
        verbose_name = _('Статья')
        verbose_name_plural = _('Статьи')
