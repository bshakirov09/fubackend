import requests


class Google:
    @staticmethod
    def validate(auth_token):
        google_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        result = requests.get(f"{google_url}?access_token={auth_token}")
        result = result.json()
        if "email" in result:
            return result
        return None
