from rest_framework import viewsets

from forms.serializers.workflow import ApproverSerializer, ApprovalWorkflowSerializer, ApprovalStepSerializer
from forms.models.workflow import Approver, ApprovalWorkflow, ApprovalStep

class ApproverSet(viewsets.ModelViewSet):

    queryset = Approver.objects.all()
    serializer_class = ApproverSerializer
    http_method_names = ['get', 'head', 'options']

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )


class ApprovalWorkflowSet(viewsets.ModelViewSet):

    queryset = ApprovalWorkflow.objects.all()
    serializer_class = ApprovalWorkflowSerializer
    http_method_names = ['post', 'get', 'put', 'patch','delete','head', 'options']

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

class ApprovalStepSet(viewsets.ModelViewSet):
    
    queryset = ApprovalStep.objects.all()
    serializer_class = ApprovalStepSerializer
    http_method_names = ['post', 'get', 'put', 'patch','delete','head', 'options']
    
    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )
