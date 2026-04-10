from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Max

from forms.serializers.submissions import FormSubmissionSerializer, FormSubmissionHistorySerializer, FormSubmissionApprovalSerializer
from forms.models.submissions import FormSubmission, FormSubmissionHistory, FormSubmissionApproval
from forms.models.audit import User
from django.db import transaction
from django.utils.timezone import now

class FormSubmissionSet(viewsets.ModelViewSet):

    queryset = FormSubmission.objects.all()
    serializer_class = FormSubmissionSerializer
    http_method_names = ['post', 'get', 'put', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticated]
    lookup_field = "reference_number"
    
    def perform_create(self, serializer):
        today_str = now().date().strftime("%Y%m%d")
        form_schema = serializer.validated_data.get("form_schema")
        print(serializer.validated_data)
        with transaction.atomic():
            # Filter reference numbers that start with today's date
            max_ref = FormSubmission.objects.filter(
                reference_number__startswith=today_str
            ).aggregate(
                max_number=Max("reference_number")
            )["max_number"]

            if max_ref:
                # Extract numeric part after YYYYMMDD
                current_number = int(max_ref[len(today_str):]) + 1
            else:
                current_number = 1

            # Create new reference number
            reference_number = f"{today_str}{current_number:04d}"

            serializer.save(
                form_schema=form_schema,
                reference_number=reference_number
            )

    def perform_update(self, serializer):
        instance = serializer.save()

        names = self.request.data.get("pending_action_by")

        if names is not None:
            users = User.objects.filter(username__in=names)
            instance.pending_action_by.set(users)    
        
            


class FormSubmissionHistorySet(viewsets.ModelViewSet):

    queryset = FormSubmissionHistory.objects.all()
    serializer_class = FormSubmissionHistorySerializer
    http_method_names = ['post', 'get', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        reference_number = self.request.query_params.get("reference_number")

        if reference_number:
            queryset = queryset.filter(
                submission__reference_number=reference_number
            ).order_by("-version_number")[:1]

        return queryset
    
    def perform_create(self, serializer):
        with transaction.atomic():
            reference_number = serializer.validated_data.pop("reference_number")
            submission = FormSubmission.objects.get(reference_number=reference_number)

            latest_version = (
                FormSubmissionHistory.objects
                .select_for_update()
                .filter(submission=submission)
                .aggregate(max_version=Max("version_number"))["max_version"]
            )

            next_version = (latest_version or 0) + 1

            serializer.save(
                submission=submission,
                version_number=next_version
            )

class FormSubmissionApprovalSet(viewsets.ModelViewSet):

    queryset = FormSubmissionApproval.objects.all()
    serializer_class = FormSubmissionApprovalSerializer
    http_method_names = ['post', 'get', 'head', 'options']
    permission_classes = [IsAuthenticated]