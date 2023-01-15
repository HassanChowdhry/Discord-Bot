import pip._vendor.requests as requests

username = ""
url = f"https://leetcode-stats-api.herokuapp.com/{username}"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)