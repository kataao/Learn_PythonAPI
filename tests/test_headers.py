import requests


class TestHeaders:
    def test_headers(self):
        header_name = 'x-secret-homework-header'
        header_value = 'Some secret value'
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(response.headers)
        assert header_name in response.headers, f"Cannot find header with name {header_name} in the response"
        assert response.headers[header_name] == header_value, \
            f"Header value is not equal to {header_value} in the response"
