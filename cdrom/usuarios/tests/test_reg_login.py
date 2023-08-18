from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from usuarios.enums import UserAction
from usuarios.models import ClasdromUserAction
from datetime import timedelta


class TestRegLogin(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        # Crear un usuario staff
        self.user = User.objects.create_user('pedro', 'pedro@data99.com.ar', 'pedro', is_staff=True)
        self.client.raise_request_exception = False
        # crear un scraper para que haya una vista de el
        self.page_url = reverse('users-login')
        self.client.force_login(self.user)

    def test_visit_reg_login(self):
        """ Probar que un usuario staff puede entrar al
            registro de logins de todos los usuarios. """
        response = self.client.get(self.page_url)
        self.assertEqual(response.status_code, 200)
        actions = ClasdromUserAction.objects.filter(action=UserAction.LOGIN)
        self.assertEqual(len(actions), 1)
        stud_user_expected = self.user.studbook_user
        self.assertEqual(actions[0].clasdrom_user, stud_user_expected)

    def test_404_for_invalid_user_get_param(self):
        """ Probar que recibo 404 cuando manoseo la URL con filtro de usuario """
        response = self.client.get(self.page_url, QUERY_STRING='user=invalid_user_name')
        self.assertEqual(response.status_code, 404)

    def test_200_for_valid_user_get_param(self):
        """ Probar que recibo 200 cuando la URL es correcta """
        response = self.client.get(self.page_url, QUERY_STRING=f'user={self.user.username}')
        self.assertEqual(response.status_code, 200)

    def test_login_date(self):
        """Compruebe que la fecha de inicio de sesión se registra correctamente"""
        # Asegúrese de que no haya acciones de usuario registradas todavía
        actions_before_login = ClasdromUserAction.objects.count()
        self.assertEqual(actions_before_login, 1)

        # Iniciar sesión del usuario
        response = self.client.get(self.page_url)
        self.assertEqual(response.status_code, 200)

        # Verifique que se haya registrado una nueva acción de usuario
        # con la acción INICIO DE SESIÓN y la marca de tiempo correcta
        actions = ClasdromUserAction.objects.filter(action=UserAction.LOGIN)
        self.assertEqual(len(actions), 1)
        action = actions[0]
        action_time = action.created_at
        # obtener el usuario de django de la accion
        user = action.clasdrom_user.user
        login_time = user.last_login
        self.assertLessEqual(login_time - action_time, timedelta(seconds=1))

    def test_logout_date(self):
        """Compruebe que la fecha de cierre de sesión se registra correctamente"""
        # Iniciar sesión del usuario
        self.client.force_login(self.user)
        response = self.client.get(self.page_url)
        self.assertEqual(response.status_code, 200)

        # Asegúrese de que no haya acciones de usuario registradas todavía
        actions_before_logout = ClasdromUserAction.objects.count()
        self.assertEqual(actions_before_logout, 2)

        # Cerrar sesión del usuario
        self.client.logout()

        # Verifique que se haya registrado una nueva acción de usuario con la acción LOGOUT y la marca de tiempo correcta
        actions = ClasdromUserAction.objects.filter(action=UserAction.LOGOUT)
        self.assertEqual(len(actions), 1)
        action = actions[0]
        action_time = action.created_at
        user = action.clasdrom_user.user
        login_time = user.last_login
        self.assertLessEqual(login_time - action_time, timedelta(seconds=1))
