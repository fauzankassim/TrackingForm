from rest_framework import viewsets
from accounts.serializers.user import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewset(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
