from rest_framework import serializers
from forms.models.forms import FormType, FormSchema

class FormTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FormType
        fields = ["url", "name", "is_active"]


class FormSchemaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FormSchema
        fields = ["url", "form_type", "schema", "version"]