from django.urls import include, path
from rest_framework.routers import DefaultRouter

from forms.views.forms import FormTypeSet, FormSchemaSet

router = DefaultRouter()
router.register(r'formtype', FormTypeSet)
router.register(r'formschema', FormSchemaSet)

urlpatterns = router.urls
