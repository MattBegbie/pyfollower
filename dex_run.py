from urllib.parse import urlparse
from urllib.parse import parse_qs
import datetime
from time import sleep, strptime
from time import time

import requests

# program modules
import dex_read_write as read_write
import dex_request

# sandbox or not
IS_SANDBOX = True
# dexcom only updates every 5 minutes, so dont request more than that
REFRESH_MINS = 5
REFRESH_SECS = REFRESH_MINS * 60


client_info = {
    "client_id": "",
    "client_secret": "",
    "redirect_uri": "",
    "response_type": "",
    "code": "",
    "timestamp": "",
}


def create_base_url():
    if IS_SANDBOX:
        baseURL = "https://sandbox-api.dexcom.com"
    else:
        baseURL = "https://api.dexcom.com"
    return baseURL


def get_client_info(baseURL=create_base_url()):
    user_info = {}

    print("\nEnter Client ID: ")
    user_info["client_id"] = input()

    print("\nEnter redirect URI: ")
    user_info["redirect_uri"] = input()

    print("\nEnter Client Secret: ")
    user_info["client_secret"] = input()

    full_url = (
        baseURL
        + "/v2/oauth2/login?"
        + "client_id="
        + user_info["client_id"]
        + "&redirect_uri="
        + user_info["redirect_uri"]
        + "&response_type=code&scope=offline_access"
    )

    print("\nGo to following link:\t\t" + full_url)
    print("\nEnter url from redirect: ")
    redirect_code_url = input()
    user_info["code"] = parse_qs(urlparse(redirect_code_url).query)["code"][0]

    user_info["timestamp"] = time()
    # timestamp()
    print(user_info["timestamp"])
    return user_info


def main():
    #     i = datetime.now()
    #     print(datetime.now())
    #     sleep(5)
    #     print(datetime.now())
    #     print(datetime.now() - i)
    # check for prerequisites
    baseURL = create_base_url()
    client_info = read_write.read_client_info()
    authorization = read_write.read_authorization()

    if authorization is not None and client_info is not None:
        print("good")

    else:
        print("bad")
        client_info = get_client_info(baseURL)
        print(client_info)
        read_write.write_client_info(client_info)
        print("making first request")
        authorization = dex_request.request_authorization(client_info, baseURL)
        read_write.write_authorization(authorization)

    # everything is set up, time for main loop
    # currTime, lastToken
    if "error" in authorization:
        print("error in authorization")
        authorization = dex_request.request_authorization(client_info, baseURL)
        read_write.write_authorization(authorization)
        print(authorization)
        exit(1)
    while 1:
        current_time = time()
        timestamp = client_info["timestamp"]
        timeChange = current_time - timestamp
        if timeChange >= REFRESH_SECS:
            print("making new token")
            # authorization = dex_request.request_authorization(
            # client_info, baseURL)
            authorization = dex_request.request_refresh(
                client_info, authorization, baseURL
            )
            client_info["timestamp"] = time()
            read_write.write_client_info(client_info)

        else:
            bs = dex_request.request_blood_glucose_estimate(
                client_info, authorization, baseURL
            )
            read_write.write_blood_sugars(bs)
            print("making request")
            print("timedifference: ")
            print(timeChange)
            sleep(REFRESH_SECS / 2)


if __name__ == "__main__":
    start_time = datetime.datetime.now().strftime("%y-%m-%dT%H:%m:%S")
    end_time = datetime.datetime.now() - datetime.timedelta(
        days=1, minutes=10
    )  # minus old
    end_time_converted = end_time.strftime("%y-%m-%dT%H:%m:%S")
    print(start_time)
    print(end_time)
    print(end_time_converted)
    main()
