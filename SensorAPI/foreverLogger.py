#import logging
##logging.basicConfig(level=logging.INFO)
from suds.client import Client
import time
import requests
from API import *
import json
import csv
import datetime
import pdb
url_sys = 'http://webctrl.bucknell.edu/_common/webservices/System?wsdl'
url_eval = 'http://webctrl.bucknell.edu/_common/webservices/Eval?wsdl'
url_trend = 'http://webctrl.bucknell.edu/_common/webservices/Trend?wsdl'
sclient = Client(url_sys, username = 'amarchiori', password = 'coggathe')
eclient = Client(url_eval, username = 'amarchiori', password = 'coggathe')
tclient = Client(url_trend, username = 'amarchiori', password = 'coggathe')
client = SensorClient()
granddad = '/trees/geographic'

####LOGGING
# set root logger to debug, to use for output
##logging.root.setLevel(logging.DEBUG)
##logging.getLogger('suds.client').setLevel(logging.INFO)
##logging.getLogger('suds.transport').setLevel(logging.INFO)
##logging.getLogger('suds.xsd.schema').setLevel(logging.INFO)
##logging.getLogger('suds.xsd.query').setLevel(logging.INFO)
##logging.getLogger('suds.metrics').setLevel(logging.INFO)
##logging.getLogger('suds.wsdl').setLevel(logging.INFO)
#logging.debug("{} wsdl:".format("-"*30))
#logging.debug(str(client))
# for svc in client.wsdl.services:
#     logging.debug("{} found service {}".format("-"*30, svc.name))
#     for port in svc.ports:
#         logging.debug("{} found port {}.{}".format(" "*30, svc.name, port.name))
#         for method in port.methods:
#             logging.debug("{} found method {}.{}.{}".format(" "*30, svc.name, port.name, method))
#             
#             
#             logging.debug("{} returned: {}".format(" "*30, svc[port][method]()))
#         

''' GQL EXAMPLE
"/trees/geographic/#academic_west/#aw_building_performance/#aw_electric_meter/"
'''

''' getValue example (not used)
data = eclient.service["Eval"]["getValue"](identifier + '/' + path)
'''

def getChildren(gqlString = "") :
    if gqlString != '' :
        gqlString = '/' + str(gqlString)
    return eclient.service["Eval"]["getFilteredChildren"](str(granddad) + str(gqlString), 'WEB_GEO')

def getTrendData(start, end, gqlString = "") :
    if gqlString != '' :
        gqlString = '/' + str(gqlString)
    return tclient.service["Trend"]["getTrendData"](str(granddad) + gqlString, start, end, False ,0)

meterTypes = [
    '_electric_meter',
    '_steam_meter',
    '_hot_water_btu_meter',
    '_water_meter',
    '_gas_meter',
    '_chilled_water_btu_meter'
    '_btu_meter'
    ]

def getMeterName(name) :
    if "_electric_meter" in name :
        return 'electric'
    elif "_steam_meter" in name :
        return "steam"
    elif "_hot_water_btu_meter" in name :
        return "hot_water"
    elif "_water_meter" in name :
        return "water"
    elif "_gas_meter" in name :
        return "gas"
    elif "_chilled_water_btu_meter" in name or "chw_btu_meter" in name  : 
        return "chilled_water"
    elif '_btu_meter' :
        return 'btu_meter'
    return name

def main() :
    buildings = getChildren()
    print buildings
    catches = 0
    '''
        Collects sample between lastTime and nextTime. After collection, nextTime becomes lastTime,
        and nextTime becomes the current time. No time is missed this way
    '''
    lastTime = client.nowS() - 900
    sampleingRate = 60*15 #sampling rate in seconds
    nextTime = lastTime + sampleingRate
    print "Time left: " + str(nextTime - client.nowS()) + "seconds"
    while True :
        if client.nowS() % 10 == 0 :
            print"Time left: " + str(nextTime - client.nowS()) + " seconds"
            time.sleep(1)
        if client.nowS() >= nextTime :
            print "Time difference: " + str(nextTime - client.nowS())

            '''
                Setup for webCTRL time:
                6/10/2014 1:00:00 AM
            '''
            isPM = False
            currentTimeDT = datetime.datetime.fromtimestamp(lastTime)
            hour = currentTimeDT.hour
            if hour >= 12 :
                isPM = True
                if hour > 12 :
                    hour -= 12
                elif hour == 0 :
                    hour = 12
                
            stime = str(currentTimeDT.month) + '/'  + str(currentTimeDT.day) + '/'  +  str(currentTimeDT.year) + ' '\
                    + str(hour) + ':' + str(currentTimeDT.minute) + ':'  + str(currentTimeDT.second)
            if isPM == True:
                stime += ' PM'
            else :
                stime += ' AM'
            print stime

                
            isPM = False
            nextTimeDT = datetime.datetime.fromtimestamp(nextTime)
            hour = nextTimeDT.hour
            if hour >= 12 :
                isPM = True
                if hour > 12 :
                    hour -= 12
                elif hour == 0 :
                    hour = 12
                isPM = True
                
            etime = str(nextTimeDT.month) + '/'  + str(nextTimeDT.day) + '/' + str(nextTimeDT.year) + ' ' + \
                    str(nextTimeDT.hour) + ':' + str(nextTimeDT.minute )+ ':' + str(nextTimeDT.second)
            if isPM == True:
                etime += ' PM'
            else :
                etime += ' AM'
            print etime

                
            for j in range(len(buildings)) :
                try :
                    building = buildings[j]
                    floors = getChildren(building.referenceName)
                    for floor in floors :
                        if '_performance' in floor.referenceName : #takes all performance: gas, electrical, hot/chilled water...
                            meters = getChildren(building.referenceName + '/' + floor.referenceName)
                            for meter in meters :
                                if getMeterName(meter.referenceName) !=  meter.referenceName:
                                    try :
                                        sensors =  getChildren(building.referenceName + '/' + floor.referenceName + '/' + meter.referenceName)
                                    except Exception as e :
                                        print 'Empty data in meter : ' + str(meter)
                                        #this is normal, 
                                        print e
                                        continue
                                    i = 0
                                    for sensor in sensors :
                                        path = sensor.referenceName
                                        if '_tn' in path or '_trnd' in path:
                                            # we exclusivly use trend data
                                            name = sensor.displayName
                                            #Converting to trend friendly timestring
                                            
                                            #getting data
                                            try :
                                                data = getTrendData(stime, etime, building.referenceName + '/' + floor.referenceName + \
                                                                    '/' + meter.referenceName + '/' + path)
                                            except Exception as e :
                                                print "Trend failed"
                                                #this is normal, sometimes trends dont have values
                                                continue
                                    
                                            if data == [] :
                                                #print 'empty trend'
                                                continue

                                            # parseing data
                                            '''
                                                Data comes in as a list with timestamp and value pairs. They are not directly paired in a data type:
                                                    they're just next to each other sequentially.
                                                [6/10/2014 1:00:00 AM, 10, 6/10/2014 1:05:00 AM, 32, 6/10/2014 1:10:00 AM, 17]
                                            '''
                                            meterName = getMeterName(meter.referenceName.replace('#',''))
                                            tag = Tags("b3.Bucknell." + building.referenceName.replace('#','') \
                                                + '.resources')
                                            name = name.replace(" ", "_")
                                            tag.addTag("units", 'kwh')
                                            tag.addTag("type", path)
                                            tag.addTag("resource", meterName)
                                            datets = []
                                            values = []
                                            datet = None
                                            value = None
                                            #print data
                                            for time_and_val in range(0, len(data), 2) :
                                                if i == 1000 :
                                                    print 'pushing ' + str(i) + ' records...'
                                                    print client.batch()
                                                    print 'done'
                                                    i = 0
                                                if data[time_and_val] == 0 or data[time_and_val] == "":
                                                    # avoids empty dp problem on server end
                                                    continue
                                                value = data[time_and_val + 1]
                                                date = data[time_and_val].replace('/',' ').replace(':',' ').split(' ')
                                                #print 'val: ' + str(value)
                                                #print 'date: ' + str(date)
                                                if date[6] == 'PM' :
                                                    if int(date[3]) != 12 :
                                                        date[3] = int(date[3]) + 12
                                                else :
                                                    if date[3] == 12 :
                                                        date[3] = 0
                                                datet = datetime.datetime(year=int(date[2]),\
                                                            month= int(date[0]), day= int(date[1]), \
                                                            hour=int(date[3]), minute=int(date[4]), \
                                                            second=int(date[5]))
                                                client.pushToBuffer(client.getUTCTimestampS(datet), value, tag)
                                                i += 1
                                            
                                                
                                            print 'writing ' + str(i) + ' records...'
                                            ######Look through None data for significance
                                            #prints feedback as well as batches
                                            print client.batch()
                                            i = 0
                except Exception as e :
                    catches += 1
                    print 'catches: ' + str(catches)
                    print e
            lastTime = nextTime
            nextTime = lastTime + sampleingRate
main()
print 'catches: ' + str(catches)

