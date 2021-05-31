import uuid

from django.contrib.auth.models import User
from django.db import models


class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    earn = models.FloatField(blank=True)
    save = models.FloatField(blank=True)
    fixed = models.FloatField(blank=True)
