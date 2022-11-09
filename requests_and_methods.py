import requests

# Request without 'method' param: returns 200 Wrong method provided
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.status_code)
print(response.text)

# Request with unexpected method: returns 400
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.status_code)
print(response.text)

# Requests with 'method' param/data: return 200 {"success":"!"}
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "GET"})
print(response.status_code)
print(response.text)
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "POST"})
print(response.status_code)
print(response.text)

# Possible combinations of request types and 'method' parameter values
# DELETE request with method GET returns: Status code: 200, Text: {"success":"!"}
methods = ('GET', 'POST', 'PUT', 'DELETE')
print()
for method in methods:
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": method})
    print(f"GET request with method {method}")
    print(f"Status code: {response.status_code}, Text: {response.text}")

print()
for method in methods:
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": method})
    print(f"POST request with method {method}")
    print(f"Status code: {response.status_code}, Text: {response.text}")

print()
for method in methods:
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": method})
    print(f"PUT request with method {method}")
    print(f"Status code: {response.status_code}, Text: {response.text}")

print()
for method in methods:
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": method})
    print(f"DELETE request with method {method}")
    print(f"Status code: {response.status_code}, Text: {response.text}")
