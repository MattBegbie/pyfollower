import requests
import json
IS_SANDBOX = True
baseURL = ""


def set_base_url():
    global baseURL
    if (IS_SANDBOX):
        baseURL = "https://sandbox-api.dexcom.com"
    else:
        baseURL = "https://api.dexcom.com"
    return (baseURL)


client_info = {"": ""}
authorization = {"": ""}


def make_request():
    url = set_base_url() + "/v2/users/self/egvs"
    query = {
        "startDate": "2022-02-06T09:12:35",
        "endDate": "2022-02-06T09:12:45"
    }
    authorization_string = "Bearer " + authorization["access_token"]
    headers = {"Authorization": authorization_string}

    response = requests.get(url, headers=headers, params=query)

    data = response.json()
    print(response.status_code)
    print(data)

    return (0)


def read_authorization():
    try:
        with open("./authorization.json", "r") as f:
            data = f.read()
            global authorization
            authorization = json.loads(data)
    except IOError:
        print("IOERROR, could not find authorization.json")
        exit(1)


def read_config():
    try:
        with open("./config.json", "r") as f:
            data = f.read()
            global client_info
            client_info = json.loads(data)

    except IOError:
        print("IOERROR, could not find config.json")
        exit(1)


read_config()
read_authorization()
set_base_url()
make_request()
