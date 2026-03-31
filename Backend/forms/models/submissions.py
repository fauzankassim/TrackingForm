from django.db import models
from .audit import AuditBase, User
from .forms import FormSchema
from .workflow import Approver, ApprovalStep

# —————————————————————————
# Form Submissions
# —————————————————————————

class SubmissionStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SUBMITTED = "submitted", "Submitted"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class FormSubmission(AuditBase):
    reference_number = models.CharField(max_length=100, unique=True)
    form_schema = models.ForeignKey(
        FormSchema, on_delete=models.PROTECT, related_name="submissions"
    )
    status = models.CharField(
        max_length=20,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.DRAFT,
    )
    pending_action_by = models.ForeignKey(
        Approver,
        on_delete=models.PROTECT,
        related_name="pending_submissions",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.reference_number

    class Meta:
        db_table = "form_submissions"


# —————————————————————————
# Form Submission History
# —————————————————————————

class FormSubmissionHistory(AuditBase):
    submission = models.ForeignKey(
        FormSubmission, on_delete=models.PROTECT, related_name="history"
    )
    content = models.JSONField()
    version_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.submission.reference_number} v{self.version_number}"

    class Meta:
        db_table = "form_submission_history"
        ordering = ["-version_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["submission", "version_number"],
                name="unique_submission_version",
            )
        ]

    @classmethod
    def get_latest(cls, submission):
        return (
            cls.objects
            .filter(submission=submission)
            .order_by("-version_number")
            .first()
        )


# —————————————————————————
# Form Submission Approvals
# —————————————————————————

class ApprovalStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    SKIPPED = "skipped", "Skipped"


class FormSubmissionApproval(AuditBase):
    submission = models.ForeignKey(
        FormSubmission, on_delete=models.PROTECT, related_name="approvals"
    )
    approval_step = models.ForeignKey(
        ApprovalStep, on_delete=models.PROTECT, related_name="submission_approvals"
    )
    approver_group = models.ForeignKey(
        Approver, on_delete=models.PROTECT, related_name="submission_approvals"
    )
    actioned_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="approval_actions",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=10,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
    )
    actioned_at = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.submission.reference_number} — "
            f"Step {self.approval_step.step_order} ({self.status})"
        )

    class Meta:
        db_table = "form_submission_approvals"
        ordering = ["approval_step__step_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["submission", "approval_step"],
                name="unique_submission_approval_step",
            )
        ]