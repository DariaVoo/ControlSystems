import json

def parse_json():
    with open('request.json', "r") as read_file:
        data = json.load(read_file)
        print(data)

    return data


# response = requests.get("https://jsonplaceholder.typicode.com/todos")
# todos = json.loads(response.text)