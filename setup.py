import requests
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs

IS_SANDBOX = True

client_info = {
    "client_id": "",
    "client_secret": "",
    "redirect_uri": "",
    "response_type": "",
    "scope": "",
    "code": "",
}
baseURL = ""

# baseURL, clientID, redirectURI, responseScope, fullURL = ""


def set_base_url():
    global baseURL
    if IS_SANDBOX:
        baseURL = "https://sandbox-api.dexcom.com"
    else:
        baseURL = "https://api.dexcom.com"
    return baseURL


def write_Authorization(data):
    with open("authorization.json", "w") as outfile:
        json.dump(data, outfile)


def get_client_info():
    code_URL = baseURL + "/v2/oauth2/login?"

    print("Enter Client ID: ")
    client_info["client_id"] = input()
    clientID = "client_id=" + client_info["client_id"]

    print("\nEnter redirect URI: ")
    client_info["redirect_uri"] = input()
    redirectURI = "&redirect_uri=" + client_info["redirect_uri"]

    responseScope = "&response_type=code&scope=offline_access"

    fullURL = code_URL + clientID + redirectURI + responseScope

    print("\nGo to link following link: " + fullURL)

    print("Enter url from redirect: ")
    redirected_code_URL = input()
    redirected_code_URL = urlparse(redirected_code_URL)
    client_info["code"] = parse_qs(redirected_code_URL.query)["code"][0]
    # client_info["code"] = code
    # print(code)
    print("\nEnter client secret: ")
    client_info["client_secret"] = input()


def get_auth_code():
    auth_url = baseURL + "/v2/oauth2/token"

    body = {
        "grant_type": "authorization_code",
        "code": client_info["code"],
        "redirect_uri": client_info["redirect_uri"],
        "client_id": client_info["client_id"],
        "client_secret": client_info["client_secret"],
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    print(body)
    response = requests.post(auth_url, data=body, headers=headers)

    data = response.json()
    write_Authorization(data)
    print(data)


def write_to_file():
    config = open("./config.json", "w")
    json.dump(client_info, config)
    # config.write(str(client_info))
    config.close()


set_base_url()
try:
    f = open("./config.json", "r")
except FileNotFoundError:
    get_client_info()
    get_auth_code()
    write_to_file()
# doesn’t exist
else:
    # print(f.read())
    data = f.read()
    client_info = json.loads(data)
    print(client_info)
    get_auth_code()
# exists
# get_client_info()
# get_auth_code()
# write_to_file()
