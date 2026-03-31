from rest_framework import serializers
from forms.models.forms import FormType, FormSchema

class FormTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormType
        fields = ["id", "name", "is_active"]


class FormSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormSchema
        fields = ["id", "schema"]