from django.contrib.auth.forms import UserCreationForm


class UserCreation(UserCreationForm):
    password2 = None
