import json


def write_authorization(data):
    with open("authorization.json", "w") as outfile:
        json.dump(data, outfile)


def read_authorization():
    try:
        with open("./authorization.json", "r") as infile:
            data = infile.read()
            authorization = json.loads(data)
            return (authorization)
    except IOError:
        print("IOERROR, could not find authorization.json")
        return (1)


def write_client_info(data):
    with open("client.json", "w") as outfile:
        json.dump(data, outfile)


def read_client_info():
    try:
        with open("./client.json", "r") as infile:
            data = infile.read()
            client_info = json.loads(data)
            return (client_info)
    except IOError:
        print("IOERROR, could not find client.json")
        return ({"code": 1})
