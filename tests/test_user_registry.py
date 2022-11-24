import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserRegistry(BaseCase):
    name_length_params = (
        {'condition': 'short', 'length': 1},
        {'condition': 'long', 'length': 251}
    )
    exclude_params = ('email', 'username', 'firstName', 'lastName')

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Users with email 'vinkotov@example.com' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'testemailexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('username', name_length_params)
    def test_create_user_with_incorrect_username_length(self, username):
        data = self.prepare_registration_data(username=self.generate_random_string(username['length']))

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too {username['condition']}", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('exclude_param', exclude_params)
    def test_create_user_with_blank_parameter(self, exclude_param):
        data = self.prepare_registration_data()
        data[exclude_param] = None

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {exclude_param}", \
            f"Unexpected response content {response.content}"
