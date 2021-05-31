from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as LoginViewNative
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from . import forms
from .mixins import LogoutMixin


class LoginView(LogoutMixin, LoginViewNative):
    template_name = "login.html"
    success_url = reverse_lazy('home')


class RegisterView(LogoutMixin, FormView):
    template_name = "register.html"
    form_class = forms.UserCreation

    def form_valid(self, form):
        messages.success(self.request, 'Conta criada com sucesso')
        form.save()
        return redirect('login')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    permission_denied_message = "Realize login"
