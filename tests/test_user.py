import pytest
import time
from api_client import ApiClient, HttpException


current_time = str(int(time.time()))
user1 = {
    "id": None,
    "username": f"test_user_{current_time}",
    "name": "test_name",
    "password": "test_password",
    "token": None
}

class TestCreateUser:
    @pytest.mark.order(1)
    def test_create_user(self, api_client: ApiClient):
        try:
            response = api_client.create_user(
                username=user1["username"],
                name=user1["name"],
                password=user1["password"]
            )
            user1["id"] = response["id"]
            assert 'id' in response
            assert response['id'] > 0
        except HttpException as e:
            if e.status_code == 409:
                user_info = api_client.get_user_by_username(user1["username"])
                user1["id"] = user_info["id"]
            else:
                raise
        return user1

    @pytest.mark.order(2)
    def test_login(self, api_client: ApiClient):
        assert user1["id"] is not None
        response = api_client.login(user1["username"], user1["password"])
        token = response['token']
        user1['token'] = token
        if hasattr(api_client, 'set_auth_token'):
            api_client.set_auth_token(token)
        assert 'token' in response
        return user1

    @pytest.mark.order(3)
    def test_get_user_by_id(self, api_client: ApiClient):
        assert user1["id"] is not None
        response = api_client.get_user_by_id(user1["id"])
        assert response["id"] == user1["id"]

    @pytest.mark.order(4)
    def test_update_user(self, api_client: ApiClient):
        pass

    @pytest.mark.order(5)
    def test_delete_user(self, api_client: ApiClient):
        pass
