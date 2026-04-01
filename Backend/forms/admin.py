from django.contrib import admin
from forms.models.forms import FormType, FormSchema
from forms.models.workflow import Approver
# Register your models here.
admin.site.register(FormType)
admin.site.register(Approver)
admin.site.register(FormSchema)