from rest_framework import viewsets

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
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

class FormSubmissionApprovalSet(viewsets.ModelViewSet):

    queryset = FormSubmissionApproval.objects.all()
    serializer_class = FormSubmissionApprovalSerializer

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )