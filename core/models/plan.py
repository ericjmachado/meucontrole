from django.contrib.auth.models import User
from django.db import models

from core.mixins import SystemModel


class Plan(SystemModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    earn = models.FloatField(blank=True, verbose_name="Ganhos (mensais)")
    save_money = models.FloatField(blank=True, verbose_name="Dinheiro desejável a poupar (mensais)")
    fixed = models.FloatField(blank=True, verbose_name="Gastos totais (mensais)")
