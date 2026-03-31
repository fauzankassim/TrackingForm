from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AuditBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="%(class)s_created"
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="%(class)s_updated"
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="%(class)s_deleted",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True