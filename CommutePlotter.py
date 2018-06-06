import matplotlib as mpl
import bokeh.plotting as bokeh
import bokeh.models as bokeh_models
import seaborn as sns

import csv
import datetime


#function definitions
def readFile(fileName):


    fileList = []

    with open(fileName, "r") as file:
        fileLines = file.readlines()
        for line in fileLines:
            #remove end line characters
            lineToAppend = line.replace("\n", "")
            lineToAppend = lineToAppend.replace("\r", "")
            lineToAppend = lineToAppend.replace("&", "and") #replace this special character
            lineToAppend = lineToAppend.replace(",", " ")

            fileList.append(lineToAppend)

    return fileList

class columnLabels:
    dateTime = 0
    dayOfWeek = 1
    origin = 2
    destination = 3
    commuteTime = 4
    distance = 5

class CommuteData:
    datetime_list = []
    hour_list = []
    dayOfWeek_list = []
    origin_list = []
    destination_list = []
    commuteTime_list = []
    distance_list = []

    def getLen(self):
        return len(self.datetime_list)

    def filterDatetime(self, indicesIn, lookFor):
        return CommuteData.filteredIndices(indicesIn, self.datetime_list, lookFor)

    def filterHour(self, indicesIn, lookFor):
        return CommuteData.filteredIndices(indicesIn, self.hour_list, lookFor)

    def filterDayOfWeek(self, indicesIn, lookFor):
        return CommuteData.filteredIndices(indicesIn, self.dayOfWeek_list, lookFor)

    def filterOrigin(self, indicesIn, lookFor):
        return CommuteData.filteredIndices(indicesIn, self.origin_list, lookFor)

    def filterDestination(self, indicesIn, lookFor):
        return CommuteData.filteredIndices(indicesIn, self.destination_list, lookFor)

    def filterCommuteTime(self, indicesIn, lookFor):
        return CommuteData.filteredIndices(indicesIn, self.commuteTime_list, lookFor)

    def filterDistance(self, indicesIn, lookFor):
        return CommuteData.filteredIndices(indicesIn, self.distance_list, lookFor)

    def buildIndexList(self):
        indexList = []
        for i in range(self.getLen()):
            indexList.append(True)
        return indexList

    @staticmethod
    def filteredIndices(indicesIn, listToFilter, lookFor):
        #output List
        indicesOut = []

        for i in range(len(listToFilter)):
            if indicesIn[i] & (listToFilter[i] == lookFor):
                indicesOut.append(True)
            else:
                indicesOut.append(False)


        return indicesOut

    @staticmethod
    def filterbyIndices(indicesIn, listToFilter):
        valuesOut = []

        for i in range(len(listToFilter)):
            if indicesIn[i]:
                valuesOut.append(listToFilter[i])

        return valuesOut


## start script ######################################################################

#file definitions
apartmentsCsv = "apartmentLocations.txt"
outputCsv = "output.csv"
workCsv = "workLocations.txt"



#load all of the info
import csv

#initialize lists
commuteData = CommuteData()

with open(outputCsv, 'r') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(csvReader, None) #skip row (header)

    # This is an array of 24 elements. Each element is another array that holds times that happened in that hour
    commuteTimeVsTimeOfDay = []
    for i in range(24):
        commuteTimeVsTimeOfDay.append([])

    for row in csvReader:
        #print(row[columnLabels.dateTime])
        datetime_str = row[columnLabels.dateTime]
        datetime_dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        hour = datetime_dt.hour
        dayOfWeek = int(row[columnLabels.dayOfWeek])
        origin = row[columnLabels.origin]
        destination = row[columnLabels.destination]
        commuteTime = float(row[columnLabels.commuteTime])
        distance = float(row[columnLabels.distance])

        commuteData.datetime_list.append(datetime_str)
        commuteData.hour_list.append(hour)
        commuteData.dayOfWeek_list.append(dayOfWeek)
        commuteData.origin_list.append(origin)
        commuteData.destination_list.append(destination)
        commuteData.commuteTime_list.append(commuteTime)
        commuteData.distance_list.append(distance)



#read list of apartments
apartmentLocations = readFile(apartmentsCsv)
workLocations = readFile(workCsv)


apartmentIndex = 0
chosenApartment = apartmentLocations[apartmentIndex]

workIndex = 0
chosenWork = workLocations[workIndex]

#hours = []
#commuteTimes = []

#for hour in range(24):
#    indexList = commuteData.buildIndexList()
#    indexList = commuteData.filterOrigin(indexList, chosenApartment)
#    indexList = commuteData.filterDestination(indexList, chosenWork)
#    indexList = commuteData.filterHour(indexList, hour)

#    commuteTimesToAdd = CommuteData.filterbyIndices(indexList, commuteData.commuteTime_list)

#    commuteTimes.extend(commuteTimesToAdd)          #append the commute times to the list
#    for i in range(len(commuteTimesToAdd)):         #append the current hour to the list
#        hours.append(hour)


#build data source
source = bokeh_models.ColumnDataSource(data=dict(
    datetime = commuteData.datetime_list,
    hour = commuteData.hour_list,
    dayOfWeek = commuteData.dayOfWeek_list,
    origin = commuteData.origin_list,
    destination = commuteData.destination_list,
    commuteTime = commuteData.commuteTime_list,
    distance = commuteData.distance_list,
))

# output to static HTML file
outputFileName = chosenApartment.replace(' ' ,'_') + '_To_' + chosenWork.replace(' ' ,'_') + '.html'
bokeh.output_file(outputFileName)

# create a new plot with a title and axis labels
title = chosenApartment + ' To ' + chosenWork
view1 = bokeh_models.CDSView(source=source, filters=[bokeh_models.GroupFilter(column_name='origin', group=chosenApartment),
                                                     bokeh_models.GroupFilter(column_name='destination', group=chosenWork)])

hover = bokeh_models.HoverTool(tooltips=[
    ("index", "$index"),
    ("(x,y)", "($x, $y)"),
    ("date", "@datetime"),
    ("dayOfWeek", "@dayOfWeek"),
    ("distance", "@distance"),
])

tools = ["box_select", hover, "reset"]
p = bokeh.figure(title=title, x_axis_label='hour of the day', y_axis_label='commute time (min)', tools=tools)

# add the plot
#p.circle(x='hour', y='commuteTime',hover_color="red", source=source, view = view1)
#ax = sns.violinplot(x='hour', y='commuteTime')

show(ax)
bokeh.save(p)
