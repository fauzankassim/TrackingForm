from forms.serializers.audit import AuditBaseSerializer
from forms.models.submissions import FormSubmission, FormSubmissionHistory, FormSubmissionApproval

class FormSubmissionSerializer(AuditBaseSerializer):
    class Meta:
        model = FormSubmission
        fields = ["id", "reference_number", "form_schema", "status", "pending_action_by"]
        read_only_fields = ["reference_number", "status", "pending_action_by"]


class FormSubmissionHistorySerializer(AuditBaseSerializer):
    class Meta:
        model = FormSubmissionHistory
        fields = ["id", "submission", "content", "version_number"]
        read_only_fields = ["version_number"]

class FormSubmissionApprovalSerializer(AuditBaseSerializer):
    class Meta:
        model = FormSubmissionApproval
        fields = ["id", "submission", "approval_step", "approver_group", "actioned_by", "status", "actioned_at", "comments"]
        read_only_fields = ["approver_group", "actioned_by", "status", "actioned_at"]

