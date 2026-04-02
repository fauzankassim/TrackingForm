from rest_framework import viewsets
from django.db import transaction
from django.db.models import Max

from forms.serializers.forms import FormTypeSerializer, FormSchemaSerializer
from forms.models.forms import FormType, FormSchema

class FormTypeSet(viewsets.ModelViewSet):

    queryset = FormType.objects.all()
    serializer_class = FormTypeSerializer
    http_method_names = ['post', 'get', 'head', 'options']


class FormSchemaSet(viewsets.ModelViewSet):

    queryset = FormSchema.objects.all()
    serializer_class = FormSchemaSerializer
    http_method_names = ['post', 'get', 'head', 'options']

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