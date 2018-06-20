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


def generatePlots(autoOpen = True):
    #read list of apartments
    apartmentLocations = readFile(apartmentsCsv)
    workLocations = readFile(workCsv)




    #read in the data
    df = pd.read_csv(outputCsv)
    df.columns = [col.replace(' ','_') for col in df.columns]
    df["Hour"] = pd.DatetimeIndex(df['Date_time']).hour     #add in an hour column with the hour of the measurement




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

    #fig = py.tools.make_subplots(rows=len(apartmentLocations), subplot_titles=apartmentLocations, cols =1)

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

        #apartment as origin
        df_filtered_origin = df.query("Origin == " + '"'+chosenApartment+'"')

        #apartment as destination
        df_filtered_apart_destination = df.query("Destination == " + '"'+chosenApartment+'"')


        for workIndex in range(len(workLocations)):
            chosenWork = workLocations[workIndex]

            #commute to wirk
            df_filtered = df_filtered_origin.query("Destination == " + '"' + chosenWork + '"')

            df_filtered_work_destination_weekday = df_filtered.query("Day_of_Week <= 5")

            #weekday to work
            trace = dict(
                type='box',
                x=df_filtered_work_destination_weekday["Hour"],
                y=df_filtered_work_destination_weekday["Time_(min)"],
                xaxis='x1',
                yaxis='y1',
                mode='markers',
                name=chosenWork + "to work",
                fillcolor= colors[workIndex],
                boxmean='sd'


                #xaxis='xaxis' + str(apartmentIndex + 1),
                #yaxis='yaxis' + str(apartmentIndex + 1),
                #transforms=transformList
            )

            data.append(trace)

            # weekend to work
            df_filtered_work_destination_weekend = df_filtered.query("Day_of_Week > 5")
            trace = dict(
                type='box',
                x=df_filtered_work_destination_weekend["Hour"],
                y=df_filtered_work_destination_weekend["Time_(min)"],
                xaxis='x1',
                yaxis='y1',
                mode='markers',
                name=chosenWork + "to work weekend",
                fillcolor=colors[workIndex],
                boxmean='sd'

                # xaxis='xaxis' + str(apartmentIndex + 1),
                # yaxis='yaxis' + str(apartmentIndex + 1),
                # transforms=transformList
            )

            data.append(trace)


            #commute home
            df_filtered_work_origin = df_filtered_apart_destination.query("Origin == " + '"' + chosenWork + '"')
            df_filtered_work_origin_weekday = df_filtered_work_origin.query("Day_of_Week <= 5")
            trace = dict(
                type='box',
                x=df_filtered_work_origin_weekday["Hour"],
                y=df_filtered_work_origin_weekday["Time_(min)"],
                xaxis='x2',
                yaxis='y2',
                mode='markers',
                name=chosenWork + "to home",
                fillcolor=colors[workIndex],
                boxmean='sd',
                shapes=[
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

                # xaxis='xaxis' + str(apartmentIndex + 1),
                # yaxis='yaxis' + str(apartmentIndex + 1),
                # transforms=transformList
            )

            data.append(trace)

            # commute home weekend
            df_filtered_work_origin_weekend = df_filtered_work_origin.query("Day_of_Week > 5")
            trace = dict(
                type='box',
                x=df_filtered_work_origin_weekend["Hour"],
                y=df_filtered_work_origin_weekend["Time_(min)"],
                xaxis='x2',
                yaxis='y2',
                mode='markers',
                name=chosenWork + "to home weekend",
                fillcolor=colors[workIndex],
                boxmean='sd',
            )
            data.append(trace)

        plotsPerCombo = 8
        visibleList = [False]*plotsPerCombo*len(apartmentLocations)
        visibleList[plotsPerCombo*apartmentIndex:plotsPerCombo*(apartmentIndex+1)] = [True]*plotsPerCombo

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
        "subplot_titles": ('First Subplot','Second Subplot'),
        "updatemenus": updatemenus,
        "xaxis1": {
                    'domain': [0.0, 0.45],
                    'anchor': 'y1',
                    },
        "xaxis2": {
                'domain': [0.55, 1.0],
                'anchor': 'y2',
                },
        "yaxis1": {
                    'domain': [0.0, 1.0],
                    'anchor': 'x1',
                    },
        "yaxis2": {
                'domain': [0.0, 1.0],
                'anchor': 'x2',
                 },
        "shapes": [
            # to work
            {
                'type': 'rect',
                'x0': 6,
                'y0': 0,
                'x1': 10,
                'y1': 30,
                'xref':'x1',
                'yref':'y1',
                'line': {
                    'color': 'rgba(128, 0, 128, 1)',
                    'width': 2,
                },
                'fillcolor': 'rgba(128, 0, 128, 0.7)',
            },
            # back home
            {
                'type': 'rect',
                'x0': 12+3,
                'y0': 0,
                'x1': 12+8,
                'y1': 30,
                'xref':'x2',
                'yref':'y2',
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

    py.offline.plot(fig, filename='index.html', validate=False, auto_open=autoOpen)





##violin
#df_filt = df
#df_filt = df_filt.query("Origin == '" + chosenApartment +"'")
#df_filt = df_filt.query("Destination == '" + chosenWork +"'")
#fig = ff.create_violin(df_filt, data_header='Time (min)', group_header='Hour',
#                       height=500, width=5000)
#py.offline.plot(fig, filename='test.html', validate=False)
