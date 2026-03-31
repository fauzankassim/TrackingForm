from django.db import models
from .audit import AuditBase, User
from .forms import FormType

# —————————————————————————
# Approvers
# —————————————————————————

class Approver(AuditBase):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(
        User, related_name="approver_groups", blank=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "approvers"


# —————————————————————————
# Approval Workflow
# —————————————————————————

class ApprovalWorkflow(AuditBase):
    form_type = models.ForeignKey(
        FormType, on_delete=models.PROTECT, related_name="workflows"
    )
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "approval_workflows"


# —————————————————————————
# Approval Steps
# —————————————————————————

class ConditionType(models.TextChoices):
    ALL_OF = "all_of", "All Of"
    ANY_OF = "any_of", "Any Of"
    NONE = "none", "None"


class ApprovalStep(AuditBase):
    workflow = models.ForeignKey(
        ApprovalWorkflow, on_delete=models.PROTECT, related_name="steps"
    )
    approver_group = models.ForeignKey(
        Approver, on_delete=models.PROTECT, related_name="approval_steps"
    )
    step_order = models.PositiveIntegerField()
    condition_type = models.CharField(
        max_length=10,
        choices=ConditionType.choices,
        default=ConditionType.NONE,
    )
    condition_logic = models.JSONField(null=True, blank=True)
    is_optional = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.workflow.name} — Step {self.step_order}"

    class Meta:
        db_table = "approval_steps"
        ordering = ["step_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["workflow", "step_order"],
                name="unique_workflow_step_order",
            )
        ]