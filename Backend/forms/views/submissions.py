from rest_framework import viewsets
from django.db import transaction
from django.db.models import Max

from forms.serializers.submissions import FormSubmissionSerializer, FormSubmissionHistorySerializer, FormSubmissionApprovalSerializer
from forms.models.submissions import FormSubmission, FormSubmissionHistory, FormSubmissionApproval

class FormSubmissionSet(viewsets.ModelViewSet):

    queryset = FormSubmission.objects.all()
    serializer_class = FormSubmissionSerializer
    http_method_names = ['post', 'get','delete','head', 'options']

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

class FormSubmissionHistorySet(viewsets.ModelViewSet):

    queryset = FormSubmissionHistory.objects.all()
    serializer_class = FormSubmissionHistorySerializer
    http_method_names = ['post', 'get', 'delete', 'head', 'options']
    
    def perform_create(self, serializer):
        with transaction.atomic():
            submission = serializer.validated_data.get("submission")

            latest_version = (
                FormSubmissionHistory.objects
                .select_for_update()
                .filter(submission=submission)
                .aggregate(max_version=Max("version_number"))["max_version"]
            )

            next_version = (latest_version or 0) + 1

            serializer.save(
                version_number=next_version,
                created_by=self.request.user,
                updated_by=self.request.user
            )

class FormSubmissionApprovalSet(viewsets.ModelViewSet):

    queryset = FormSubmissionApproval.objects.all()
    serializer_class = FormSubmissionApprovalSerializer
    http_method_names = ['post', 'get', 'head', 'options']

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )