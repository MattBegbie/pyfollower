from urllib.parse import urlparse
from urllib.parse import parse_qs
from datetime import datetime
# program modules
import dex_read_write
import dex_request

IS_SANDBOX = True


client_info = {
    "client_id": "",
    "client_secret": "",
    "redirect_uri": "",
    "response_type": "",
    "code": "",
    "timestamp": ""
}


def create_base_url():
    if (IS_SANDBOX):
        baseURL = "https://sandbox-api.dexcom.com"
    else:
        baseURL = "https://api.dexcom.com"
    return (baseURL)


def get_client_info():
    user_info = {}

    print("\nEnter Client ID: ")
    user_info["client_id"] = input()

    print("\nEnter redirect URI: ")
    user_info["redirect_uri"] = input()

    print("\nEnter Client Secret: ")
    user_info["client_secret"] = input()

    full_url = (create_base_url()
                + "/v2/oauth2/login?"
                + "client_id=" + user_info["client_id"]
                + "&redirect_uri=" + user_info["redirect_uri"]
                + "&response_type=code&scope=offline_access")

    print("\nGo to following link:\t\t" + full_url)
    print("\nEnter url from redirect: ")
    redirect_code_url = input()
    user_info["code"] = parse_qs(urlparse(redirect_code_url).query)['code'][0]

    user_info["timestamp"] = datetime.now()

    return (user_info)


def main():
    # check for prerequisites
    baseURL = create_base_url()
    client_info = dex_read_write.read_client_info()
    authorization = dex_read_write.read_authorization()

    if authorization == 1 or client_info == 1:
        print("missing authorization or client info")

    else:
        print("authorization found")


if __name__ == '__main__':
    main()
