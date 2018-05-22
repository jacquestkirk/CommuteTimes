from apscheduler.schedulers.blocking import BlockingScheduler
from CommuteTimes import *

def some_job():
    response_json = buildRequest(apartmentLocations, workLocations)
    response_json_return = buildRequest(workLocations, apartmentLocations)

    writeResults(outputCsv, response_json, apartmentLocations, workLocations)
    writeResults(outputCsv, response_json_return, workLocations, apartmentLocations)

scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', hours=0.5)
scheduler.start()