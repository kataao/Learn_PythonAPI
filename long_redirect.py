import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
print(f"Number of redirects: {len(response.history)}")
print(*[history.url for history in response.history], sep='\n')
print(f"Final URL: {response.url}")
