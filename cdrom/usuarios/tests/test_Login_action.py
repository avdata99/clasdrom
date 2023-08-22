from django.contrib.auth.models import User
from django.test import Client, TestCase
from usuarios.enums import UserAction
from usuarios.models import ClasdromUserAction


class TestLogin(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        # Crear un usuario comun (no staff)
        self.user = User.objects.create_user('juan', 'juan@data99.com.ar', 'juan')
        self.client.raise_request_exception = False

    def test_login_generate_actions(self):
        """ Iniciar sesión como usuario """
        response = self.client.login(username='juan', password='juan')
        self.assertTrue(response)
        logins = ClasdromUserAction.objects.filter(action=UserAction.LOGIN)
        self.assertEqual(len(logins), 1)
        stud_user_expected = self.user.clasdrom_user
        self.assertEqual(logins[0].clasdrom_user, stud_user_expected)

    def test_logout_generate_actions(self):
        """ Cerrar sesión como usuario """
        response = self.client.login(username='juan', password='juan')
        self.assertTrue(response)
        self.client.logout()  # Logout the user
        logins = ClasdromUserAction.objects.filter(action=UserAction.LOGOUT)
        self.assertEqual(len(logins), 1)
        stud_user_expected = self.user.clasdrom_user
        self.assertEqual(logins[0].clasdrom_user, stud_user_expected)
