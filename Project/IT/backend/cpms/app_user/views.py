from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import UserProfileSerializer

User = get_user_model()


class UserProfileAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
