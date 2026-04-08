from django.urls import path
from accounts.views.login import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]