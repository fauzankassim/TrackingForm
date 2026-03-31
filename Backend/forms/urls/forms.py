from django.urls import include, path
from rest_framework.routers import DefaultRouter

from forms.views.forms import FormTypeSet, FormSchemaSet

router = DefaultRouter()
router.register(r'form-types', FormTypeSet, basename="form-type")
router.register(r'form-schemas', FormSchemaSet, basename="form-schema")

urlpatterns = router.urls
