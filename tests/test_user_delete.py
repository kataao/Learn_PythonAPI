from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_delete_important_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.delete("/user/2", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response2.content}"

        response3 = MyRequests.get(f"/user/2", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response3, 200)
        expected_fields = ("username", "email", "firstName", "lastName")
        Assertions.assert_json_has_keys(response3, expected_fields)

    def test_delete_just_created_user(self):
        user_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=user_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user_id = self.get_json_value(response1, "id")

        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == "User not found", \
            f"Unexpected response content {response4.content}"

    def test_delete_user_auth_as_another_user(self):
        # REGISTRY
        user1_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=user1_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user1_id = self.get_json_value(response1, "id")

        user2_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user", data=user2_data)
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")
        user2_id = self.get_json_value(response2, "id")

        # LOGIN
        login1_data = {
            'email': user1_data['email'],
            'password': user1_data['password']
        }
        response3 = MyRequests.post("/user/login", data=login1_data)
        auth_sid1 = self.get_cookie(response3, "auth_sid")
        token1 = self.get_header(response3, "x-csrf-token")

        # EDIT
        response4 = MyRequests.delete(f"/user/{user2_id}",
                                      headers={"x-csrf-token": token1}, cookies={"auth_sid": auth_sid1})
        Assertions.assert_code_status(response4, 200)

        # GET
        response5 = MyRequests.get(f"/user/{user2_id}",
                                   headers={"x-csrf-token": token1}, cookies={"auth_sid": auth_sid1})
        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_has_key(response5, "username")
