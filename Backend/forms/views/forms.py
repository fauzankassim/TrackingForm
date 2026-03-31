from rest_framework import viewsets

from forms.serializers.forms import FormTypeSerializer, FormSchemaSerializer
from forms.models.forms import FormType, FormSchema

class FormTypeSet(viewsets.ModelViewSet):

    queryset = FormType.objects.all()
    serializer_class = FormTypeSerializer

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )


class FormSchemaSet(viewsets.ModelViewSet):

    queryset = FormSchema.objects.all()
    serializer_class = FormSchemaSerializer

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )