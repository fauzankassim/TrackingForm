from django.db import models
from .audit import AuditBase

# —————————————————————————
# Form Types
# —————————————————————————

class FormType(AuditBase):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "form_types"


# —————————————————————————
# Form Schema
# —————————————————————————

class FormSchema(AuditBase):
    form_type = models.ForeignKey(
        FormType, on_delete=models.PROTECT, related_name="schemas"
    )
    schema = models.JSONField()
    version = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.form_type.name} v{self.version}"

    class Meta:
        db_table = "form_schemas"
        ordering = ["-version"]
        constraints = [
            models.UniqueConstraint(
                fields=["form_type", "version"],
                name="unique_form_type_version",
            )
        ]

