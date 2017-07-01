from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from mptt.forms import TreeNodeChoiceField
from redactor.widgets import RedactorEditor

from webapp.models import Post, Category


class PostForm(forms.ModelForm):
    category = TreeNodeChoiceField(queryset=Category.objects.all(),
                                   level_indicator=u'+--')
    image = forms.ImageField(widget=forms.FileInput, label=_('Изображение'))

    class Meta:
        model = Post
        widgets = {
            'info': RedactorEditor()
        }
        fields = ['title', 'image', 'info', 'category']
