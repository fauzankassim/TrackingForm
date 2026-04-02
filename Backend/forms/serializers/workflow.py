from forms.serializers.audit import AuditBaseSerializer
from forms.models.workflow import Approver, ApprovalWorkflow, ApprovalStep


class ApproverSerializer(AuditBaseSerializer):
    class Meta:
        model = Approver
        fields = ["id", "name", "description", "members", "is_active"]

class ApprovalWorkflowSerializer(AuditBaseSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = ["id", "form_type", "name", "is_active"]


class ApprovalStepSerializer(AuditBaseSerializer):
    class Meta:
        model = ApprovalStep
        fields = ["id", "workflow", "approver_group", "step_order", "condition_type", "condition_logic", "is_optional"]