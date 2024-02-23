import pip._vendor.requests as requests


def getLeetStats(username):
  url = f"https://leetcode-stats-api.herokuapp.com/{username}"
  response = requests.request("GET", url, headers={}, data={})
  print(response.text)