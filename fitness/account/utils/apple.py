from datetime import timedelta

import jwt
import requests
from django.conf import settings
from django.utils import timezone

from fitness.account.constants import DeviceType

SOCIAL_AUTH_APPLE_KEY_ID = settings.SOCIAL_AUTH_APPLE_KEY_ID
SOCIAL_AUTH_APPLE_TEAM_ID = settings.SOCIAL_AUTH_APPLE_TEAM_ID
CLIENT_ID = settings.APPLE_CLIENT_ID
SOCIAL_AUTH_APPLE_PRIVATE_KEY = b"""-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgSYirRWNMYX9JLc3m
yHDnk9j1V/Rvi3jIQ+7Zlc+YG6WgCgYIKoZIzj0DAQehRANCAAQEMsIWvwfhSI9U
TR9vHYo0WnZzxxWGzoT3771CDfLdRxqW96nKgLlYw/7RAy7cvv+W6XBVOfIpHCS7
nR2bhD9j
-----END PRIVATE KEY-----"""


class Apple:
    """apple authentication backend"""

    def __init__(self, device_type):
        if device_type == DeviceType.WEB:
            self.client_id = f"{CLIENT_ID}.com"
        else:
            self.client_id = f"{CLIENT_ID}.app"

    ACCESS_TOKEN_URL = "https://appleid.apple.com/auth/token"

    def do_auth(self, access_token):
        """
        Finish the auth process once the access_token was retrieved
        Get the email from ID token received from apple
        """
        client_id, client_secret = self.get_key_and_secret()
        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": access_token,
            "grant_type": "authorization_code",
        }
        res = requests.post(Apple.ACCESS_TOKEN_URL, data=data, headers=headers)
        id_token = res.json().get("id_token", None)
        if id_token:
            decoded = jwt.decode(
                id_token, "", options={"verify_signature": False}
            )
            email = decoded.get("email")
            if email:
                data = dict(
                    email=email,
                    first_name=decoded.get("first_name"),
                    last_name=decoded.get("last_name"),
                )
                return data
        return None

    def get_key_and_secret(self):
        headers = {"kid": SOCIAL_AUTH_APPLE_KEY_ID, "alg": "ES256"}

        payload = {
            "iss": SOCIAL_AUTH_APPLE_TEAM_ID,
            "iat": int(timezone.now().strftime("%s")),
            "exp": int((timezone.now() + timedelta(days=180)).strftime("%s")),
            "aud": "https://appleid.apple.com",
            "sub": self.client_id,
        }

        client_secret = jwt.encode(
            payload,
            SOCIAL_AUTH_APPLE_PRIVATE_KEY,
            algorithm="ES256",
            headers=headers,
        )

        return self.client_id, client_secret
