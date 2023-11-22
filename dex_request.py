import requests


def request_authorization(client_info, baseURL):
    url = baseURL + "/v2/oauth2/token"

    body = {
        "grant_type": "authorization_code",
        "code": client_info["code"],
        "redirect_uri": client_info["redirect_uri"],
        "client_id": client_info["client_id"],
        "client_secret": client_info["client_secret"]
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    print(body)
    response = requests.post(url, data=body, headers=headers)

    data = response.json()
    print(data)
    return (data)


def request_refresh(client_info, authorization, baseURL):
    url = baseURL + "/v2/oauth2/token"

    body = {
        "grant_type": "refresh_token",
        "refresh_token": authorization["refresh_token"],
        "redirect_uri": client_info["redirect_uri"],
        "client_id": client_info["client_id"],
        "client_secret": client_info["client_secret"]
    }

    print(body)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=body, headers=headers)

    data = response.json()

    print(data)
    return (data)


def request_blood_glucose_estimate(client_info, authorization, baseURL):
    url = baseURL + "/v2/users/self/egvs"
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

    return (data)
