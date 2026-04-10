from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Max, Q

from forms.serializers.submissions import FormSubmissionSerializer, FormSubmissionHistorySerializer, FormSubmissionApprovalSerializer
from forms.models.submissions import FormSubmission, FormSubmissionHistory, FormSubmissionApproval
from forms.models.audit import User
from django.db import transaction
from django.utils.timezone import now
from rest_framework.response import Response
from django.db.models.functions import Substr, Cast
from django.db.models import IntegerField

class FormSubmissionSet(viewsets.ModelViewSet):

    queryset = FormSubmission.objects.all()
    serializer_class = FormSubmissionSerializer
    http_method_names = ['post', 'get', 'put', 'patch', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticated]
    lookup_field = "reference_number"
    
    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = FormSubmission.objects.filter(
            Q(created_by=user) | Q(pending_action_by=user)
        ).distinct()

        require_approval = request.query_params.get("require_approval")

        if require_approval == "true":
            queryset = queryset.filter(
                pending_action_by=request.user,
                status="submitted"
            )
        else:
            queryset = queryset.filter(created_by=request.user)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        today_str = now().date().strftime("%Y%m%d")
        form_schema = serializer.validated_data.get("form_schema")

        with transaction.atomic():
            last = (
                FormSubmission.objects
                .filter(reference_number__startswith=today_str)
                .annotate(
                    num_part=Cast(
                        Substr("reference_number", 9),
                        IntegerField()
                    )
                )
                .order_by("-num_part")
                .first()
            )

            if last:
                current_number = int(last.reference_number[8:]) + 1
            else:
                current_number = 1

            reference_number = f"{today_str}{current_number:04d}"

            serializer.save(
                form_schema=form_schema,
                reference_number=reference_number
            )

    def perform_update(self, serializer):
        instance = self.get_object()
        user = self.request.user

        status = self.request.data.get("status")

        is_approver = instance.pending_action_by.filter(id=user.id).exists()

        if is_approver and status in ["approved", "rejected"]:
            serializer.save(status=status)

            return 
        if instance.created_by == user:
            instance = serializer.save()
            names = self.request.data.pop("pending_action_by_names")
            if names is not None:
                users = User.objects.filter(username__in=names)
                instance.pending_action_by.set(users)

            return
            


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