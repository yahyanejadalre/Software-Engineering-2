import requests
from django.conf import settings

EMSP_API_URL = settings.EMSP_API_URL
LOGIN_URL = EMSP_API_URL + 'user/token/'


def get_authenticate_token():
    response = requests.post(LOGIN_URL, data={'username': settings.EMSP_USERNAME, 'password': settings.EMSP_PASSWORD})

    response.raise_for_status()

    if response.status_code == 200:
        return response.json()['access']


def send_authenticated_request(method, url, **kwargs):
    token = get_authenticate_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.request(method, url, headers=headers, **kwargs)

    try:
        response.raise_for_status()
    except:  # noqa
        raise Exception("emsp is not available")

    return response
