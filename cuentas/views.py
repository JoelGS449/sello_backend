from rest_framework.generics import RetrieveAPIView
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import LoginSerializer, UsuarioSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'


class YoView(RetrieveAPIView):
    serializer_class = UsuarioSerializer

    def get_object(self):
        return self.request.user
