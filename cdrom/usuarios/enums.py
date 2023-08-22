from django.db import models


class UserAction(models.TextChoices):
    LOGIN = 'LI'
    LOGOUT = 'LO'
    SEARCH = 'SE'
