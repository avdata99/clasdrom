from django.contrib.auth import views as auth_views
from django.urls import path
from .views import HomePage, LoginPageView, MySettingsView


urlpatterns = [
    path('', HomePage.as_view(), name='base'),
    # Login and logout pages
    path('login', LoginPageView.as_view(), name='login-page'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    # My Settings
    path('my-settings', MySettingsView.as_view(), name='my-settings'),

]
