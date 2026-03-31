from django.urls import include, path
from rest_framework.routers import DefaultRouter

from forms.views.workflow import ApproverSet, ApprovalWorkflowSet, ApprovalStepSet

router = DefaultRouter()
router.register(r'approvers', ApproverSet, basename='approver')
router.register(r'approval-workflows', ApprovalWorkflowSet, basename='approval-workflow')
router.register(r'approval-steps', ApprovalStepSet, basename='approval-step')

urlpatterns = router.urls
