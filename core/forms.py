from django.contrib.auth.forms import UserCreationForm as UserForm
from django import forms

from core.models import Plan, Expense


class UserCreationForm(UserForm):
    password2 = None


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ("earn", 'save_money', 'fixed')


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ("name", "value", "description", "date",)
