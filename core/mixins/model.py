import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet, Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UUIDPkFieldMixin(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name=_('uuid'), default=uuid.uuid4,
                          editable=False, unique=True)

    class Meta:
        abstract = True

    @property
    def get_pk(self):
        return str(self.id)


class TimeManagerMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, )
    modified_at = models.DateTimeField(auto_now=True, )

    class Meta:
        abstract = True


class UniqueTogetherManagerMixin(models.Model):
    class Meta:
        abstract = True

    class UniqueTogether:
        value = ()

    @staticmethod
    def __depth__(t):
        depths = [UniqueTogetherManagerMixin.__depth__(item) for item in t if isinstance(item, tuple)]
        if len(depths) > 0:
            return 1 + max(depths)
        return 1

    def save(self, *args, **kwargs):
        if bool(self.UniqueTogether.value):
            unique = self.UniqueTogether.value
            Klass = self.__class__
            args_to_check = []

            if self.__depth__(unique) > 1:
                pass
            else:
                for param in unique:
                    args_to_check.append(Q(**{param: getattr(self, param)}))
            qs = Klass.objects.filter(~Q(pk=self.get_pk), Q(deleted_at__isnull=True), *args_to_check)
            if qs.exists():
                raise ValidationError({"error": "Os campos %s devem ser únicos" % ", ".join(unique)})
        return super(UniqueTogetherManagerMixin, self).save(*args, **kwargs)


class ParanoiaQuerySet(QuerySet):
    """
    Prevents objects from being hard-deleted. Instead, sets the
    ``date_deleted``, effectively soft-deleting the object.
    """

    def delete(self):
        for obj in self:
            obj.deleted_at = timezone.now()
            obj.save()


class ParanoiaManager(models.Manager):
    """
    Only exposes objects that have NOT been soft-deleted.
    """

    def get_queryset(self):
        return ParanoiaQuerySet(self.model, using=self._db).filter(
            deleted_at__isnull=True)


class ParanoiaMixin(models.Model):
    class Meta:
        abstract = True

    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = models.Manager()
    objects_without_deleted = ParanoiaManager()

    def delete(self, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    @property
    def get_deleted_str(self):
        return ' - Deletado' if self.deleted_at else ''


class SystemModel(TimeManagerMixin,
                  UUIDPkFieldMixin,
                  ParanoiaMixin,
                  UniqueTogetherManagerMixin,
                  models.Model):
    class Meta:
        abstract = True
