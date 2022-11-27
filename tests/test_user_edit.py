import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    edit_user_negative_params = (
        {'key': 'email', 'value': 'testemailexample.com', 'error': 'Invalid email format'},
        {'key': 'firstName', 'value': 'a', 'error': '{"error":"Too short value for field firstName"}'}
    )

    edit_user_params = (
        {'key': 'username', 'value': 'Changed Username'},
        {'key': 'firstName', 'value': 'Changed First Name'},
        {'key': 'lastName', 'value': 'Changed Last Name'}
    )

    def test_edit_just_created_user(self):
        # REGISTRY
        registry_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=registry_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = registry_data['email']
        first_name = registry_data['firstName']
        password = registry_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = 'Changed Name'

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={'firstName': new_name}
                                   )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response4, "firstName", new_name,
                                             "Wrong name of the user after edit")

    def test_edit_user_details_not_auth(self):
        data = self.prepare_registration_data()
        response = MyRequests.put("/user/2", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('edit_param', edit_user_params)
    def test_edit_user_details_auth_as_another_user(self, edit_param):
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

        # LOGIN 1
        login1_data = {
            'email': user1_data['email'],
            'password': user1_data['password']
        }
        response3 = MyRequests.post("/user/login", data=login1_data)
        auth_sid1 = self.get_cookie(response3, "auth_sid")
        token1 = self.get_header(response3, "x-csrf-token")

        # EDIT
        response4 = MyRequests.put(f"/user/{user2_id}",
                                   headers={"x-csrf-token": token1},
                                   cookies={"auth_sid": auth_sid1},
                                   data={edit_param['key']: edit_param['value']}
                                   )
        Assertions.assert_code_status(response4, 200)

        # LOGIN 2
        login2_data = {
            'email': user2_data['email'],
            'password': user2_data['password']
        }
        response5 = MyRequests.post("/user/login", data=login2_data)
        auth_sid2 = self.get_cookie(response5, "auth_sid")
        token2 = self.get_header(response5, "x-csrf-token")

        # GET
        response6 = MyRequests.get(f"/user/{user2_id}",
                                   headers={"x-csrf-token": token2},
                                   cookies={"auth_sid": auth_sid2})
        Assertions.assert_json_value_by_name(
            response6,
            edit_param['key'],
            user2_data[edit_param['key']],
            "Wrong name of the user after edit. Another user should not be able to change user details"
        )

    @pytest.mark.parametrize('edit_param', edit_user_negative_params)
    def test_edit_user_negative(self, edit_param):
        # REGISTRY
        user_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=user_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={edit_param['key']: edit_param['value']}
                                   )
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == edit_param['error'], \
            f"Unexpected response content {response3.content}"

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(
            response4,
            edit_param['key'],
            user_data[edit_param['key']],
            "Wrong name of the user after edit. User details should not be updated by invalid data"
        )
