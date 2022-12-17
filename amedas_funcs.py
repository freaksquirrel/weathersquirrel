# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import os.path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import datetime as dt
import json
import amedas_config as a_cfg

#Note: seems like past data is only available for the 10 days previous to current day

# Create a URL to request weather data based on a date and time (datatime format)
def createRequestUrlFromDatetime( target_datetime = "" ):
    if( not isinstance(target_datetime, dt.datetime) ): target_datetime = dt.datetime.now()
    datetime_str = target_datetime.strftime('%Y%m%d%H%M')
    amedas_req_url = a_cfg.url_format.replace(a_cfg.replace_target, datetime_str)
    return amedas_req_url

# Create a URL to request weather data based on a date and time (datatime format)
def createRequestUrlFromString( target_datetime = "" ):
    if( target_datetime == ""): target_datetime = dt.datetime.now().strftime('%Y%m%d%H')
    amedas_req_url = a_cfg.url_format.replace(a_cfg.replace_target, target_datetime)
    return amedas_req_url

# Request weather data from created URL and put the JSON result, if valid, on a dictionary
def requestWeatherData( target_datetime = "", area_code = 0 ):
    # check the date & time parameter first
    if( isinstance(target_datetime, dt.datetime) ):
        req_url = createRequestUrlFromDatetime(target_datetime)
    else:
        # Unless specified on a string, by default request the weather for the current datetime but time as HH:00
        if( target_datetime == "" ) : target_datetime = dt.datetime.now().strftime('%Y%m%d%H00')    
        req_url = createRequestUrlFromString(target_datetime)
    # lets try and see if we can actually get a result from the server
    try:
        weather_response = urlopen(req_url)
    except HTTPError as e:
        print('HTTP ERROR... code: ', e.code)
        area_weather_info = "ERROR"
    except URLError as e:
        print('URL ERROR... reason: ', e.reason)
        area_weather_info = "ERROR"
    else:
        raw_data = json.loads(weather_response.read().decode("utf-8"))
        #use the dafault area code unless specified
        if( not area_code ): area_code = a_cfg.area_code
        if( area_code in raw_data ):
            area_weather_info = raw_data[area_code]
        else:
            area_weather_info = "NAN"
            
    return area_weather_info

# add the response to a JSON file having all the data we collect from AMEDAS
def addWeatherValueEntry( datapoint, debugprint = False, area_code = 0, entry_datetime = "" ):
    #check if datapoint is a dict type
    if( type(datapoint) is not dict ): return False
    #Get data from file
    try:
        if( os.path.exists(a_cfg.amedas_log) ):
            #Open file in read only mode only
            tempfile = open(a_cfg.amedas_log, 'r')
            tempdata = json.load(tempfile)
            tempfile.close()
            if( debugprint == True) : print('Reading data from file {} \n'.format(a_cfg.amedas_log))
        else:
            tempdata = {}
            if( debugprint == True) : print('New file will be created at {} \n'.format(a_cfg.amedas_log))
    except ValueError:
        if( debugprint == True) : print('File {} was empty \n creating new entry...\n'.format(a_cfg.amedas_log))
        print('Empty temp file')
        tempdata = {}
    except IOError:
        print('Unexpected error: {}'.format(sys.exc_info()[0:2]))

    if( isinstance(entry_datetime, dt.datetime) ):
        #Get the entry datetime to create a JSON key for searching
        entry_time_key = entry_datetime.strftime('%Y-%m-%d %H:%M')
        #Get the entry date to create a JSON key for searching
        entry_date_key = entry_datetime.strftime('%Y-%m-%d')
        #use the dafault area code unless specified
        if( not area_code ): area_code = a_cfg.area_code
        #Add the rest of the info to the data point before adding it
        datapoint_full = {entry_time_key : {str(area_code):datapoint}}
        
        #search the date key in the current data        
        if( entry_date_key in tempdata ):
            #if( entry_time_key in tempdata[entry_date_key] ):
            tempdata[entry_date_key].update(datapoint_full)
            # consider checking if value for that time is already in the list or not
            if( debugprint == True) :print('Added the datapoint {} to the key {} \n'.format(datapoint_full, entry_date_key))
        else:
            #if not available, add new date key and add datapoint
            tempdata.update({entry_date_key:datapoint_full})
            # consider checking if value for that time is already in the list or not
            if( debugprint == True) : print('Created the key {} and added the datapoint {} \n'.format(entry_date_key, datapoint_full))
        #finally, re-write json file
        tempfile = open(a_cfg.amedas_log,'w')
        json.dump(tempdata, tempfile, sort_keys=True)
        if( debugprint == True) : print('Re-wrote data to file {} \n'.format(a_cfg.amedas_log))
        tempfile.close()
        return True
    else:
        print("error")
        return False

# to make my life easier... just put the request and add entry functions together ;)    
def requestAndStoreWeatherInfo( target_datetime = "", area_code = 0, debugprint = True):
    res = False
    #just in case... check the params and create some values if required
    if( not isinstance(target_datetime, dt.datetime) ): target_datetime = dt.datetime.now()
    if( not area_code ): area_code = a_cfg.area_code
    # Reques the data from the server
    weather_data = requestWeatherData( target_datetime, area_code)
    print('Got data {}'.format(weather_data))
    #now check if the result is valid or not
    if( weather_data ):
        # Storage with debug mode... will call it on a cron-job and keep a log
        res = addWeatherValueEntry( weather_data, debugprint, area_code, target_datetime )
        print('Got data for the area {} at @ ({}) = {}'.format(area_code, target_datetime, res))
    else:
        print('Error! not able to get data for the area {} at @ ({}) = {}'.format(area_code, target_datetime, res))
    return res

