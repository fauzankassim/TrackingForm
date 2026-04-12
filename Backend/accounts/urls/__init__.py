from .user import urlpatterns as user_urls
from .auth import urlpatterns as login_urls

urlpatterns = ( user_urls + login_urls )