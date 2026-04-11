from forms.serializers.audit import AuditBaseSerializer
from forms.models.submissions import FormSubmission, FormSubmissionHistory, FormSubmissionApproval
from rest_framework import serializers

class FormSubmissionSerializer(AuditBaseSerializer):
    form_type = serializers.CharField(write_only=True)
    pending_action_by_names = serializers.ListField(
        write_only=True,
        required=False
    )
    class Meta:
        model = FormSubmission
        fields = ["id", "reference_number", "form_type", "form_schema", "status", "pending_action_by", "pending_action_by_names"]
        read_only_fields = ["reference_number", "pending_action_by", "form_schema"]


class FormSubmissionHistorySerializer(AuditBaseSerializer): 
    reference_number = serializers.CharField(write_only=True)
    class Meta:
        model = FormSubmissionHistory
        fields = ["id", "submission", "reference_number", "content", "version_number"]
        read_only_fields = ["submission", "version_number"]

class FormSubmissionApprovalSerializer(AuditBaseSerializer):
    class Meta:
        model = FormSubmissionApproval
        fields = ["id", "submission", "approval_step", "approver_group", "actioned_by", "status", "actioned_at", "comments"]
        read_only_fields = ["approver_group", "actioned_by", "status", "actioned_at"]

