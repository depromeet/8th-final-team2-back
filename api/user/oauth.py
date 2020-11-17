import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
import google.oauth2.credentials
import google_auth_oauthlib.flow

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
                "property_keys": ["properties.nickname", "properties.profile_image", "kakao_account.profile"]
            },
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
            }
        )

        if res.status_code != 200:
            return None

        data = res.json()
        kakao_uid = data.get("id")

        u, created = User.objects.get_or_create(
            provider=Provider.KAKAO, uid=kakao_uid)

        if created:
            u.username = get_random_alphanumeric_string(10, 5)

            properties = data.get("properties")
            if properties:
                nickname = properties.get("nickname")
                profile_image = properties.get("profile_image")

                if nickname:
                    u.nickname = nickname
                if profile_image:
                    image_name = urlparse(profile_image).path.split('/')[-1]
                    image_response = requests.get(profile_image)

                    if image_response.status_code == 200:
                        u.image.save(image_name, ContentFile(
                            image_response.content), save=True)
            u.save()

        return u


class Google(OAuthBase):
    def get_user(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            "",
            scopes=["openid", "'https://www.googleapis.com/auth/userinfo.profile'"],
            state='12345678910',
        )
        flow.redirect_uri = 'http://127.0.0.1:8000/'
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')

        if res.status_code != 200:
            return None

        data = res.json()
        google_uid = data.get("id")

        u, created = User.objects.get_or_create(
            provider=Provider.GOOGLE, uid=google_uid)

        if created:
            u.username = get_random_alphanumeric_string(10, 5)

            u.save()

        return u
