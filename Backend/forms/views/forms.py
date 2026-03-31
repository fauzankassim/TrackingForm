from rest_framework import viewsets

from forms.serializers.forms import FormTypeSerializer, FormSchemaSerializer
from forms.models.forms import FormType, FormSchema

class FormTypeSet(viewsets.ModelViewSet):

    queryset = FormType.objects.all()
    serializer_class = FormTypeSerializer


class FormSchemaSet(viewsets.ModelViewSet):

    queryset = FormSchema.objects.all()
    serializer_class = FormSchemaSerializer