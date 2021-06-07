from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as LoginViewNative, LogoutView as LogoutViewNative
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from . import forms
from . import models
from .mixins import LogoutMixin


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
        qp = self.request.GET
        year_selected = qp.get('year', now.year)
        month_selected = qp.get('month', now.month)
        expense_filter = qp.get('expense')
        kwargs['months'] = [{"label": value, "value": index + 1} for index, value in enumerate(months)]
        kwargs['month_selected'] = int(month_selected)
        kwargs['years'] = [i for i in range(2021, 2031)]
        kwargs['year_selected'] = int(year_selected)
        kwargs['expense'] = ''

        expenses = models.Expense.objects.filter(user=self.request.user,
                                                 date__month=month_selected,
                                                 date__year=year_selected).order_by('-date')

        if expense_filter:
            kwargs['expense'] = expense_filter
            expenses = expenses.filter(name__icontains=expense_filter)

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


class LogoutView(LogoutMixin, LogoutViewNative):

    def get_next_page(self):
        return reverse_lazy('login')
