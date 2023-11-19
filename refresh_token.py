import requests
import json

IS_SANDBOX = True
client_info = {}
authorization = {}


def set_base_url():
    if (IS_SANDBOX):
        baseURL = "https://sandbox-api.dexcom.com"
    else:
        baseURL = "https://api.dexcom.com"
    return (baseURL)


def read_client_info():
    try:
        with open("./config.json", "r") as f:
            data = f.read()
            global client_info
            client_info = json.loads(data)
    except IOError:
        print("IOERROR, could not find config.json")
        exit(1)


def read_authorization():
    try:
        with open("./authorization.json", "r") as f:
            data = f.read()
            global authorization
            authorization = json.loads(data)
    except IOError:
        print("IOERROR, could not find authorization.json")
        exit(1)


def send_refresh():
    url = set_base_url() + "/v2/oauth2/token"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": authorization["refresh_token"],
        "redirect_uri": client_info["redirect_uri"],
        "client_id": client_info["client_id"],
        "client_secret": client_info["client_secret"]
    }

    print(payload)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=payload, headers=headers)

    data = response.json()

    print(data)

# def set_refresh_token():
#
# #
# #
#
# def set_access_token():
#
# #
# #
#


def write_new_authorization():
    if len(authorization) == 0:
        print("ERROR, empty dictionary")
        exit(1)
    with open("/authorization.json", "w") as f:
        json.dump(authorization, f)

        # config = open('./config.json', "w")
    # json.dump(client_info, config)
    # # config.write(str(client_info))
    # config.close()
    #


read_authorization()
read_client_info()
send_refresh()
