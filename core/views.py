from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as LoginViewNative
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from . import forms
from .mixins import LogoutMixin
from . import models


class LoginView(LogoutMixin, LoginViewNative):
    template_name = "login.html"
    success_url = reverse_lazy('home')


class RegisterView(LogoutMixin, FormView):
    template_name = "register.html"
    form_class = forms.UserCreationForm

    def form_valid(self, form):
        messages.success(self.request, 'Conta criada com sucesso')
        form.save()
        return redirect('login')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        months = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro',
            'Novembro', 'Dezembro'
        ]
        now = datetime.now()
        kwargs['months'] = [{"label": value, "value": index + 1} for index, value in enumerate(months)]
        kwargs['month_selected'] = now.month
        kwargs['years'] = [i for i in range(2021, 2031)]
        kwargs['year_selected'] = now.year
        expenses = models.Expense.objects.filter(user=self.request.user).order_by('date')
        paginator = Paginator(expenses, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        kwargs['page_obj'] = page_obj
        return super(HomeView, self).get_context_data(**kwargs)


class PlanView(LoginRequiredMixin, FormView):
    template_name = "plan.html"
    form_class = forms.PlanForm

    def get_form(self, form_class=None):
        Plan = models.Plan
        if form_class is None:
            form_class = self.get_form_class()
        try:
            plan = Plan.objects.get(user=self.request.user)
            return self.form_class(instance=plan, **self.get_form_kwargs())
        except Plan.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        messages.success(self.request, 'Plano salvo com sucesso')
        return redirect('home')


class ExpenseView(LoginRequiredMixin, FormView):
    template_name = "expense.html"
    form_class = forms.ExpenseForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        messages.success(self.request, 'Despesas salvo com sucesso')
        return redirect('home')
