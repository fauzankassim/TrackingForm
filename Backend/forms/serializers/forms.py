from forms.serializers.audit import AuditBaseSerializer
from forms.models.forms import FormType, FormSchema

class FormTypeSerializer(AuditBaseSerializer):
    class Meta:
        model = FormType
        fields = ["id", "name", "is_active"]
        read_only_fields = ["is_active"]


class FormSchemaSerializer(AuditBaseSerializer):
    class Meta:
        model = FormSchema
        fields = ["id", "form_type", "schema", "version"]
        read_only_fields = ["version"]
        validators = []