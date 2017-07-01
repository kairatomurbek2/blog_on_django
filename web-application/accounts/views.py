from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from accounts import forms
from main.parameters import Messages


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm

    def get(self, request):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(request.GET.get('next', reverse('home')))
        form = self.form_class(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(request.GET.get('next', reverse(('home'))))
        return render(request, self.template_name, {'form': form})


class RegistrationView(CreateView):
    template_name = 'accounts/registration.html'
    success_message = Messages.Registration.adding_success
    form_class = forms.RegistrationForm

    def get(self, request):
        if not self.request.user.is_authenticated():
            return render(request, self.template_name, {'form': self.form_class})
        return HttpResponseRedirect(request.GET.get('next', reverse('home')))

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(RegistrationView, self).form_valid(form)

    def get_success_url(self):
        return reverse('login')
