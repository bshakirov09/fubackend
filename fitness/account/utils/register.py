import secrets

from rest_framework.exceptions import ValidationError

from fitness.account.constants import GENDER, AuthType
from fitness.account.models import User


def generate_password():
    password_length = 15
    return secrets.token_urlsafe(password_length)


def register_social_user(email, first_name, last_name, device):
    users = User.objects.filter(email=email)
    if users.exists():
        user = users.first()
        if user.auth_type != AuthType.SOCIAL:
            raise ValidationError("Your already registered with your email")
        if device and device not in user.devices:
            user.devices.append(device)
            user.save()
    else:
        if first_name is None:
            first_name = email.split("@")[0]
        if last_name is None:
            last_name = ""
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=GENDER.FEMALE,
            password=generate_password(),
            auth_type=AuthType.SOCIAL,
        )
    return {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "auth_type": user.auth_type,
        "gender": user.gender,
        "tokens": user.tokens(),
    }
