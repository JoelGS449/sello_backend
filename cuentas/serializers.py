from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()
    perfil = serializers.SerializerMethodField()
    herramientas = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nombre', 'email', 'perfil', 'herramientas']

    def get_nombre(self, obj):
        return obj.get_full_name() or obj.username

    def get_perfil(self, obj):
        return obj.perfil.nombre if obj.perfil else None

    def get_herramientas(self, obj):
        return list(obj.herramientas_permitidas().values_list('slug', flat=True))


class LoginSerializer(TokenObtainPairSerializer):
    """Devuelve los tokens junto con el usuario para no hacer una segunda petición."""

    def validate(self, attrs):
        data = super().validate(attrs)
        data['usuario'] = UsuarioSerializer(self.user).data
        return data
