import json


def write_authorization(data):
    with open("authorization.json", "w") as outfile:
        json.dump(data, outfile)
        return 0


def read_authorization():
    try:
        with open("./authorization.json", "r") as infile:
            data = infile.read()
            authorization = json.loads(data)
            return authorization
    except IOError:
        print("IOERROR, could not find authorization.json")
        return None


def write_client_info(data):
    with open("client.json", "w") as outfile:
        json.dump(data, outfile)
        return 0


#
# config = open('./config.json', "w")
#     json.dump(client_info, config)
#     # config.write(str(client_info))
#     config.close()


def read_client_info():
    try:
        with open("./client.json", "r") as infile:
            data = infile.read()
            client_info = json.loads(data)
            return client_info
    except IOError:
        print("IOERROR, could not find client.json")
        return None


def write_blood_sugars(data):
    with open("blood.json", "w") as outfile:
        json.dump(data, outfile)
        return 0
