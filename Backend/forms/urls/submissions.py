from django.urls import include, path
from rest_framework.routers import DefaultRouter

from forms.views.submissions import FormSubmissionSet, FormSubmissionHistorySet, FormSubmissionApprovalSet

router = DefaultRouter()
router.register(r'submissions', FormSubmissionSet, basename='submission')
router.register(r'submissions-history', FormSubmissionHistorySet, basename='submission-history')
router.register(r'submissions-approval', FormSubmissionApprovalSet, basename='submission-approval')

urlpatterns = router.urls
