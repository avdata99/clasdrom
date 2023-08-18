from django.urls import path
from usuarios.views import  UserSystemView, UserActionLoginView, UsersCSVView


urlpatterns = [

    path('user-login', UserActionLoginView.as_view(), name='users-login'),
    # Lista de los usuarios del systema
    path('app-users', UserSystemView.as_view(), name='users-system'),
    path('downloads/users.csv', UsersCSVView.as_view(), name='users_csv'),

]
