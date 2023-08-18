from django.test import TestCase
from django.contrib.auth.models import User
from usuarios.models import ClasdromUsuario


class TestUserSignal(TestCase):

    def test_user_signal(self):
        """ Probar que se crea el StudBookUser cuando se crea el User. """
        user = User.objects.create_user('tes_user', 'test@user.com', 'test_password')
        stud_users = ClasdromUsuario.objects.filter(user=user)
        self.assertEqual(stud_users.count(), 1)
        self.assertEqual(user.clasdrom_user.user, user)

    def test_no_duplicated(self):
        """ Probar que no se crea un StudBookUser cuando se crea un User si ya existe. """
        user = User.objects.create_user('tes_user', 'test@user.com', 'test_password')
        user.first_name = 'Test'
        user.save()
        stud_users = ClasdromUsuario.objects.filter(user=user)
        self.assertEqual(stud_users.count(), 1)
        stud_users = ClasdromUsuario.objects.all()
        self.assertEqual(stud_users.count(), 1)
