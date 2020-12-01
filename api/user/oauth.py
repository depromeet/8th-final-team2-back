import requests
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from apps.user.enums import Provider
from apps.user.models import User
from utils.random import get_random_alphanumeric_string


class OAuthBase:
    def __init__(self, token):
        self.token = token

    def get_user(self):
        raise NotImplementedError("need get_user method")


class Kakao(OAuthBase):
    def get_user(self):
        url = "https://kapi.kakao.com/v2/user/me"
        res = requests.post(
            url,
            {
                "property_keys": [
                    "properties.nickname",
                    "properties.profile_image",
                    "kakao_account.profile",
                ]
            },
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            },
        )

        if res.status_code != 200:
            return None

        data = res.json()
        kakao_uid = data.get("id")

        u, created = User.objects.get_or_create(provider=Provider.KAKAO, uid=kakao_uid)

        if created:
            u.username = get_random_alphanumeric_string(10, 5)
            u.save()

        return u


class Google(OAuthBase):
    def __init__(self, token):
        super().__init__(token)

        self.clientId = settings.GOOGLE_CLIENT_ID

    def get_user(self):
        try:
            id_info = id_token.verify_oauth2_token(
                self.token, google_requests.Request(), self.clientId
            )
        except ValueError:
            return None

        google_uid = id_info.get("sub", None)

        u, created = User.objects.get_or_create(
            provider=Provider.GOOGLE, uid=google_uid
        )

        if created:
            u.username = get_random_alphanumeric_string(10, 5)
            u.save()

        return u