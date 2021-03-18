import json

def parse_json():
    with open('/home/dvoo/ControlSystems/lab1/request_manual.json', "r") as read_file:
        data = json.load(read_file)
    return data


# response = requests.get("https://jsonplaceholder.typicode.com/todos")
# todos = json.loads(response.text)