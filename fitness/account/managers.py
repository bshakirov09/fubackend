from django.contrib.auth.base_user import BaseUserManager
from django.template.loader import render_to_string

from fitness.account.constants import AuthType
from fitness.account.utils.mail import send_email


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        email = extra_fields.pop("email")
        if self.filter(email=email).exists():
            self.get(email=email).delete()
        password = extra_fields.pop("password")
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def is_username_unique(self, username):
        return not self.filter(username=username).exists()

    def delete_inactive_user(self, email):
        self.filter(email=email, is_active=False).delete()

    def register_user(self, data):
        self.delete_inactive_user(data["email"])
        data.setdefault("is_active", False)
        data.pop("confirm_password")
        data["auth_type"] = AuthType.EMAIL
        user = self.create_user(**data)
        code = self.model.generate_code()
        self.model.set_cache(str(user.email), code)
        subject = "Verification code"
        message = render_to_string(
            "account/email.html",
            {"code": code, "message": "Your verification code is"},
        )
        send_email.delay(user.email, subject, message)
        data.pop("password")
        data.pop("auth_type")
        data.pop("is_active")
        return {
            "type": "CONFIRMATION_REQUIRED",
            "info": data,
        }
