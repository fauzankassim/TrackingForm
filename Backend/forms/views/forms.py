from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Max
from rest_framework.response import Response
from forms.serializers.forms import FormTypeSerializer, FormSchemaSerializer
from forms.models.forms import FormType, FormSchema

class FormTypeSet(viewsets.ModelViewSet):

    queryset = FormType.objects.all()
    serializer_class = FormTypeSerializer
    http_method_names = ['post', 'get', 'head', 'options']
    permission_classes = [IsAuthenticated]


class FormSchemaSet(viewsets.ModelViewSet):

    queryset = FormSchema.objects.all()
    serializer_class = FormSchemaSerializer
    http_method_names = ['post', 'get', 'head', 'options']
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = FormSchema.objects.all()
        form_type = self.request.query_params.get("form_type")

        if form_type:
            queryset = (
                queryset
                .filter(form_type__slug = form_type)
                .order_by("-version")[:1]
            )
            
        else:
            queryset = queryset.filter(created_by=user)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if "form_type" in request.query_params:
            instance = queryset.first()
            if not instance:
                return Response(None)  # or {} or 404 depending on your design
        
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

    def perform_create(self, serializer):
        with transaction.atomic():
            form_type = serializer.validated_data.get("form_type")

            latest_version = (
                FormSchema.objects
                .select_for_update()
                .filter(form_type=form_type)
                .aggregate(max_version=Max("version"))["max_version"]
            )

            next_version = (latest_version or 0) + 1

            serializer.save(
                version=next_version,
            )