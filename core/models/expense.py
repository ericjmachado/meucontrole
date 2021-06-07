from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from core.mixins import SystemModel


class Expense(SystemModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(verbose_name="Nome da despesa", max_length=255)
    value = models.FloatField(verbose_name="Valor", validators=[MinValueValidator(0.01)])
    description = models.TextField(verbose_name="Descrição", blank=True)
    date = models.DateField(blank=True, verbose_name="Data da despesa", default=datetime.today)
