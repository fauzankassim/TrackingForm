from django.contrib import admin
from forms.models.forms import FormType, FormSchema
from forms.models.workflow import Approver, ApprovalWorkflow, ApprovalStep
from forms.models.submissions import FormSubmission, FormSubmissionHistory, FormSubmissionApproval

# Register your models here.
class AuditAdmin(admin.ModelAdmin):
    audit_readonly_fields = ('id', 'created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_by', 'deleted_at',)

    def get_readonly_fields(self, request, obj=None):
        base = super().get_readonly_fields(request, obj)
        return tuple(base) + self.audit_readonly_fields

@admin.register(FormType)
class FormTypeAdmin(AuditAdmin):
    pass

@admin.register(FormSchema)
class FormSchemaAdmin(AuditAdmin):
    pass

@admin.register(Approver)
class ApproverAdmin(AuditAdmin):
    pass

@admin.register(ApprovalWorkflow)
class ApprovalWorkflowAdmin(AuditAdmin):
    pass

@admin.register(ApprovalStep)
class ApprovalStepAdmin(AuditAdmin):
    pass

@admin.register(FormSubmission)
class FormSubmissionAdmin(AuditAdmin):
    readonly_fields = ('pending_action_by',)

@admin.register(FormSubmissionHistory)
class FormSubmissionHistoryAdmin(AuditAdmin):
    readonly_fields = ('version_number',)

@admin.register(FormSubmissionApproval)
class FormSubmissionApprovalAdmin(AuditAdmin):
    readonly_fields = ('actioned_by', 'actioned_at',)
