import pandas as pd
import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np

apartmentsCsv = "apartmentLocations.txt"
outputCsv = "output.csv"
workCsv = "workLocations.txt"

#colors for Wells Fargo and SpaceX respectively
colors = ['red','blue']

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



#read list of apartments
apartmentLocations = readFile(apartmentsCsv)
workLocations = readFile(workCsv)




#read in the data
df = pd.read_csv(outputCsv)
df["Hour"] = pd.DatetimeIndex(df['Date time']).hour     #add in an hour column with the hour of the measurement




#select locations
apartmentIndex = 0
chosenApartment = apartmentLocations[apartmentIndex]

workIndex = 0
chosenWork = workLocations[workIndex]

#build up filters
#originFilter = dict(
#    type = 'filter',
#    target = df['Origin'],
#    operation = '=',
#    value = chosenApartment
#  )

destinationFilter = dict(
    type = 'filter',
    target = df['Destination'],
    operation = '=',
    value = chosenWork
  )

destinationGroup = dict(
        type = 'groupby',
        groups = df['Destination'])

fig = py.tools.make_subplots(rows=len(apartmentLocations), subplot_titles=apartmentLocations, cols =1)

data = []
buttons = []
#partmentLocations = apartmentLocations[0:4]
for apartmentIndex in range(len(apartmentLocations)):
    chosenApartment = apartmentLocations[apartmentIndex]

    originFilter = dict(
        type='filter',
        target=df['Origin'],
        operation='=',
        value=chosenApartment
    )

    transformList = [originFilter, destinationGroup]

    df_filtered_origin = df.query("Origin == " + '"'+chosenApartment+'"')


    for workIndex in range(len(workLocations)):
        chosenWork = workLocations[workIndex]
        df_filtered = df_filtered_origin.query("Destination == " + '"' + chosenWork + '"')

        trace = dict(
            type='scatter',
            x=df_filtered["Hour"],
            y=df_filtered["Time (min)"],
            mode='markers',
            name=chosenWork,
            fillcolor= colors[workIndex]

            #xaxis='xaxis' + str(apartmentIndex + 1),
            #yaxis='yaxis' + str(apartmentIndex + 1),
            #transforms=transformList
        )

        data.append(trace)

    visibleList = [False]*2*len(apartmentLocations)
    visibleList[2*apartmentIndex:2*apartmentIndex+2] = [True, True]

    button = dict(label=chosenApartment,
                  method='update',
                  args=[{'visible': visibleList},
                        {'title': chosenApartment}])

    buttons.append(button)

updatemenus = list([
    dict(active=-1,
         buttons=buttons,
    )
])

layout = {
    "title": "CommuteTimes",
    "updatemenus": updatemenus,
    'shapes': [
        # filled Rectangle
        {
            'type': 'rect',
            'x0': 6,
            'y0': 0,
            'x1': 10,
            'y1': 30,
            'line': {
                'color': 'rgba(128, 0, 128, 1)',
                'width': 2,
            },
            'fillcolor': 'rgba(128, 0, 128, 0.7)',
        },
    ]
}

fig = {
    "data": data,
    "layout": layout
}

py.offline.plot(fig, filename=chosenApartment+'.html', validate=False)





##violin
#df_filt = df
#df_filt = df_filt.query("Origin == '" + chosenApartment +"'")
#df_filt = df_filt.query("Destination == '" + chosenWork +"'")
#fig = ff.create_violin(df_filt, data_header='Time (min)', group_header='Hour',
#                       height=500, width=5000)
#py.offline.plot(fig, filename='test.html', validate=False)
