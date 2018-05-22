import requests
import pytz
import datetime
import Config

apartmentsCsv = "apartmentLocations.txt"
workCsv = "workLocations.txt"

outputCsv = "output.csv"



def readFile(fileName):


    fileList = []

    with open(fileName, "r") as file:
        fileLines = file.readlines()
        for line in fileLines:
            #remove end line characters
            lineToAppend = line.replace("\n", "")
            lineToAppend = lineToAppend.replace("\r", "")
            lineToAppend = lineToAppend.replace("&", "and") #replace this special character

            fileList.append(lineToAppend)

    return fileList


def buildArgumentString(argumentList):

    argumentString = ""

    for i in range(len(argumentList)):
        arg = argumentList[i]

        argumentString += arg.replace(" ", "+")

        if (i != len(argumentList)-1):
            argumentString += "|"

    return argumentString


def buildRequest(origins, destinations):
    baseRequest = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    originsInput = "origins=" + buildArgumentString(origins) + "&"
    destinationsInput = "destinations=" + buildArgumentString(destinations) + "&"
    keyInput = "key="+Config.api_key + "&"
    otherInputs = "units=imperial&departure_time=now"

    requestCombined = baseRequest + originsInput + destinationsInput + keyInput + otherInputs
    print(requestCombined)

    response = requests.post(requestCombined)

    return response.json()

def writeResults(resutFile, response_json, origins, destinations):

    with open(resutFile, "a+") as file:
        for i in range(len(response_json["rows"])):
            originJson = response_json["rows"][i]
            for j in range(len(originJson["elements"])):
                destinationJson = originJson["elements"][j]

                #parse and put together string

                timeStamp_pst = datetime.datetime.now(pytz.timezone('US/Pacific'))
                timeStamp_pst_str = timeStamp_pst.strftime("%Y-%m-%d %H:%M:%S")

                dayOfWeek = timeStamp_pst.weekday()


                time_s = destinationJson["duration_in_traffic"]["value"]
                time_min = float(time_s)/60

                distance_m = destinationJson["distance"]["value"]
                distance_miles = float(distance_m)/1609.34

                origin = origins[i]
                origin_cleaned = origin.replace(",", " ")

                destination = destinations[j]
                destination_cleaned = destination.replace(",", " ")

                stringToWrite = timeStamp_pst_str + "," +\
                                str(dayOfWeek) + "," +\
                                origin_cleaned + "," +\
                                destination_cleaned + "," +\
                                str(time_min) + "," +\
                                str(distance_miles)

                file.write("\n" + stringToWrite)






apartmentLocations = readFile(apartmentsCsv)

workLocations = readFile(workCsv)




if __name__ == "__main__":
    from CommuteTimes import *
    response_json = buildRequest(apartmentLocations, workLocations)
    response_json_return = buildRequest(workLocations, apartmentLocations)

    writeResults(outputCsv, response_json, apartmentLocations, workLocations)
    writeResults(outputCsv, response_json_return, workLocations, apartmentLocations)
