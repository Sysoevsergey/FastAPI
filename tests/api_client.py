import requests


class HttpException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _call(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        response = requests.request(method, url, **kwargs)
        if response.status_code >= 400:
            raise HttpException(response.status_code, response.text)
        return response.json()


    def get_user_by_id(self, user_id: int):
        return self._call("GET", f"/api/v1/user/{user_id}/")

    def create_user(self, username: str, name: str, password: str):
        return self._call("POST", "/api/v1/user/", json={"username": username,"name": name, "password": password})

    def login(self, username: str, password: str):
        return self._call("POST", "/api/v1/login/", json={"username": username, "password": password})

    def update_user(self, user_id: int, name: str, password: str):
        return self._call("PATCH", f"/api/v1/user/{user_id}/", json={"name": name, "password": password})

    def delete_user(self, user_id: int):
        return self._call("DELETE", f"/api/v1/user/{user_id}/")


    def get_advertisement(self, advertisement_id: int):
        pass

    def create_advertisement(self, title: str, description: str, price: int, author: str):
        pass

    def find_advertisements(self, title: str | None = None, description: str | None = None, price: int | None = None):
        pass

    def update_advertisement(
        self, advertisement_id: int, title: str | None = None, description: str | None = None, price: int | None = None
    ):
        pass

    def delete_advertisement(self, advertisement_id: int):
        pass
