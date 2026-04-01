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

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

class ApprovalStepSet(viewsets.ModelViewSet):
    
    queryset = ApprovalStep.objects.all()
    serializer_class = ApprovalStepSerializer

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )
