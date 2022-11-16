import requests


class TestCookie:
    def test_cookie(self):
        cookie_name = 'HomeWork'
        cookie_value = 'hw_value'
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the response"
        assert response.cookies[cookie_name] == cookie_value, \
            f"Cookie value is not equal to {cookie_value} in the response"

