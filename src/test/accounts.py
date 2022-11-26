import requests
from datetime import datetime
import unittest
from postgres_air.config import settings

base_url = "http://0.0.0.0"


def _get_token():
    headers = {"accept": "application/json"}
    data = {
        "grant_type": "",
        "username": settings.TEST_USER,
        "password": settings.TEST_PASSWORD,
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }
    response = requests.post(base_url + "/auth/sign-in", headers=headers, data=data)
    return response.json()["access_token"]


def _create_session():
    session = requests.session()
    session.headers.update(
        {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {_get_token()}",
        }
    )
    return session


class SessionFactory(object):
    def __init__(self):
        self.session = None
        self.token = None

    def get_session(self):
        if not self.session:
            self.session = _create_session()
        return self.session


class TestAccounts(unittest.TestCase):
    url = base_url + "/api/accounts"
    sf = SessionFactory()
    session = sf.get_session()

    def test_create_account(self):
        json_data = {
            "login": "nexter83",
            "first_name": "Oleg",
            "last_name": "Basmanov",
            "update_ts": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f"),
        }
        response = self.session.post(self.url, json=json_data)
        self.assertEqual(201, response.status_code)

    def test_get_accounts(self):
        response = self.session.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_get_account(self):
        response = self.session.get(self.url + "/257337")
        self.assertEqual(200, response.status_code)

    def test_update_account(self):
        json_data = {
            "login": "nexter83",
            "first_name": "Oleg",
            "last_name": "Basmanov",
            "update_ts": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f"),
        }
        response = self.session.put(self.url + "/257337", json=json_data)
        self.assertEqual(200, response.status_code)

    def test_delete_account(self):
        last_account_id = (
            self.session.get(
                self.url + "?order_column=account_id&is_desc=true&limit=1&offset=0"
            )
            .json()
            .get("items")[0]["account_id"]
        )
        response = self.session.delete(self.url + f"/{last_account_id}")
        self.assertEqual(204, response.status_code)


if __name__ == "__main__":
    unittest.main()
