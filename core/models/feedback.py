from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from core.mixins import SystemModel


class Expense(SystemModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

