import json

data = {
    "name" : "Xander",
    "age" : 19,
    "school" : "FEU TECH"

}

with open ("app_log_test.json", "w") as file:
    json.dump(data, file, indent=4)

with open("app_log_test.json", "r") as file:
    printed_data = json.load(file)
    print(printed_data) 
 