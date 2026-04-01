from rest_framework import serializers
from forms.models.submissions import FormSubmission, FormSubmissionHistory, FormSubmissionApproval

class FormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormSubmission
        fields = ["id", "reference_number", "form_schema", "status", "pending_action_by"]
        read_only_fields = ["reference_number", "status", "pending_action_by"]


class FormSubmissionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FormSubmissionHistory
        fields = ["id", "submission", "content", "version_number"]
        read_only_fields = ["version_number"]

class FormSubmissionApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormSubmissionApproval
        fields = ["id", "submission", "approval_step", "approver_group", "actioned_by", "status", "actioned_at", "comments"]

