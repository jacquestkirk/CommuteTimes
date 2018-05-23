import Config
import requests
import json


superMartketNames = ["Ralphs", "Vons", "WholeFoods", "Sprouts", "TraderJoes"]
outputFile = "supermarkets.csv"
location = "33.805192,-118.351390"
radius = "15000"
radius_gym_m = "800"

#initialize data dictionary
data = {}
data['supermarkets']=[]

#add in grocery stores
with open(outputFile, "w") as file:
    for i in range(len(superMartketNames)):
        request_str = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        request_str += "location=" + location + "&"
        request_str += "radius=" + radius + "&"
        request_str += "keyword=" + superMartketNames[i] + "&"
        request_str += "key=" +Config.api_key

        print(request_str)

        response = requests.post(request_str)
        response_json = response.json()

        for j in range(len(response_json["results"])):
            name = response_json["results"][j]["name"]
            address = response_json["results"][j]["vicinity"]

            #find location
            lattitude = response_json["results"][j]["geometry"]["location"]["lat"]
            longitude = response_json["results"][j]["geometry"]["location"]["lng"]
            location = str(lattitude) + "," + str(longitude)

            stringToWrite = name + "," + address

            file.write("\n" + stringToWrite)

            supermarket = {}
            supermarket["name"] = name
            supermarket["address"] = address
            supermarket["location"] = location
            supermarket["gyms"] = []
            supermarket["coffeeShops"] = []

            data['supermarkets'].append(supermarket)


for i in range(len(data['supermarkets'])):
    supermarket = data['supermarkets'][i]
    supermarketLocation = supermarket["location"]

    request_str = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    request_str += "location=" + supermarketLocation + "&"
    request_str += "radius=" + radius_gym_m + "&"
    request_str += "keyword=" + "gym" + "&"
    request_str += "key=" + Config.api_key

    print(request_str)
    response = requests.post(request_str)
    response_json = response.json()

    for j in range(len(response_json["results"])):
        name = response_json["results"][j]["name"]
        address = response_json["results"][j]["vicinity"]

        #build json
        gym = {}
        gym["name"] = name
        gym["address"] = address

        supermarket["gyms"].append(gym)

jsonString = json.dumps(data)
print(jsonString)