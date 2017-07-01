from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise ValidationError(
                _("Пользователь с таким email уже существует"),
                code='email_used'
            )
        return data

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
