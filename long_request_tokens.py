import requests
from json.decoder import JSONDecodeError
import time

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
print(response.status_code)
parsed_response = None
try:
    parsed_response = response.json()
    print(parsed_response)
except JSONDecodeError:
    print("Response is not a JSON format")
if parsed_response is not None:
    seconds = parsed_response['seconds']
    token = parsed_response['token']

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={'token': token})
parsed_response = None
try:
    parsed_response = response.json()
except JSONDecodeError:
    print("Response is not a JSON format")
if parsed_response is not None and 'status' in parsed_response:
    actual_status = parsed_response['status']
    expected_status = "Job is NOT ready"
    print(f"status is correct: {actual_status}") if actual_status == expected_status \
        else print(f"status is incorrect: {actual_status}, should be {expected_status}")
else:
    print(f"Response is incorrect: {response.text}")

time.sleep(seconds)
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={'token': token})
parsed_response = None
try:
    parsed_response = response.json()
except JSONDecodeError:
    print("Response is not a JSON format")
if parsed_response is not None and 'status' in parsed_response:
    actual_status = parsed_response['status']
    actual_result = parsed_response['result']
    expected_status = "Job is ready"
    expected_result = "42"
    print(f"status is correct: {actual_status}") if actual_status == expected_status \
        else print(f"status is incorrect: {actual_status}, should be {expected_status}")
    print(f"result is correct: {actual_result}") if actual_result == expected_result \
        else print(f"result is incorrect: {actual_result}, should be {expected_result}")
else:
    print(f"Response is incorrect: {response.text}")
