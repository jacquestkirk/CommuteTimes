from CommuteTimes import *
from CommutePlotterBox import *

response_json = buildRequest(apartmentLocations, workLocations)
response_json_return = buildRequest(workLocations, apartmentLocations)

writeResults(outputCsv, response_json, apartmentLocations, workLocations)
writeResults(outputCsv, response_json_return, workLocations, apartmentLocations)

generatePlots(autoOpen=False, pushToPlotly=True)