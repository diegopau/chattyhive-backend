try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    get_user_model = lambda: User  # noqa


def get_username(user):
    return user.profile.public_name
