from .forms import urlpatterns as forms_urls
from .submissions import urlpatterns as submissions_urls
from .workflow import urlpatterns as workflow_urls

urlpatterns = (
    forms_urls 
    + submissions_urls
    + workflow_urls
)