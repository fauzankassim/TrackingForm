from .user import urlpatterns as user_urls
from .login import urlpatterns as login_urls

urlpatterns = ( user_urls + login_urls )