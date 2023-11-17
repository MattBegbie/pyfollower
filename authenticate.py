import requests

url = "https://api.dexcom.com/v2/oauth2/token"

payload = {
  "grant_type": "string",
  "code": "string",
    "redirect_uri": "authorization_code",
  "client_id": "string",
  "client_secret": "string"
}

headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.post(url, data=payload, headers=headers)

data = response.json()
print(data)
