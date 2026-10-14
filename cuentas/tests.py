from django.test import TestCase
from rest_framework.test import APIClient

from .models import Herramienta, Perfil, Usuario


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        perfil = Perfil.objects.create(nombre='Fotógrafo')
        perfil.herramientas.add(Herramienta.objects.get(slug='marca'))
        Usuario.objects.create_user('ana', password='secreta-123', perfil=perfil)

    def login(self, password='secreta-123'):
        return self.client.post('/api/auth/login/', {'username': 'ana', 'password': password})

    def test_login_devuelve_tokens_y_herramientas_del_perfil(self):
        res = self.login()
        self.assertEqual(res.status_code, 200)
        self.assertIn('access', res.data)
        self.assertEqual(res.data['usuario']['perfil'], 'Fotógrafo')
        self.assertEqual(res.data['usuario']['herramientas'], ['marca'])

    def test_login_con_contrasena_incorrecta(self):
        self.assertEqual(self.login('mala').status_code, 401)

    def test_yo_requiere_token(self):
        self.assertEqual(self.client.get('/api/auth/yo/').status_code, 401)
        token = self.login().data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(self.client.get('/api/auth/yo/').data['username'], 'ana')

    def test_usuario_sin_perfil_no_tiene_herramientas(self):
        Usuario.objects.create_user('sin', password='secreta-123')
        res = self.client.post('/api/auth/login/', {'username': 'sin', 'password': 'secreta-123'})
        self.assertEqual(res.data['usuario']['herramientas'], [])
