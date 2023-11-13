# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import os.path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import datetime as dt
import json
import amedas_config as a_cfg

#Note: seems like past data on AMEDAS is only available for the 10 days previous to current day

# Create a URL to request weather data based on a date and time (datatime format)
def createRequestUrlFromDatetime( target_datetime = "" ):
    if( not isinstance(target_datetime, dt.datetime) ): target_datetime = dt.datetime.now()
    datetime_str = target_datetime.strftime('%Y%m%d%H%M')
    amedas_req_url = a_cfg.url_format.replace(a_cfg.replace_target, datetime_str)
    return amedas_req_url


# Create a URL to request weather data based on a date and time (datatime format)
def createRequestUrlFromString( target_datetime = "" ):
    # Unless specified on the string, by default use current datetime but time as HH:00
    if( target_datetime == ""):
        target_datetime = dt.datetime.now().strftime('%Y%m%d%H00')
    else:
        try:           
            dt.datetime.strptime( target_datetime, '%Y%m%d%H%M' )
        except ValueError as e:
            print(f"Error: {e}")
            target_datetime = dt.datetime.now().strftime('%Y%m%d%H00')
            print(f"Using datetime.now() with time as HH:00 instead -> {target_datetime}")
    amedas_req_url = a_cfg.url_format.replace(a_cfg.replace_target, target_datetime)
    return amedas_req_url


# Form the path to the log where the entry must be saved or where the graphs are to be stored
def buildPathFromDate( target_datetime = "", target = "", areacode = 'common' ):
    if( target in ["g","l"] ):  # "g" for graphs path, "l" for log path
        if( target_datetime == "" ):
            target_datetime = dt.datetime.now()#.strftime('%Y-%m-%d')
        elif ( not isinstance(target_datetime, dt.datetime) ):
            try:           
                target_datetime = dt.datetime.strptime( target_datetime, '%Y-%m-%d' )
            except ValueError as e:
                print(f"Error: {e}")
                target_datetime = dt.datetime.now()
                print(f"Using datetime.now() instead -> {target_datetime}")
        else:
            print(f"Target date = {target_datetime}")
        entry_year = target_datetime.strftime('%Y')
        entry_month = target_datetime.strftime('%m')
        if( target == "l"):
            targetpath = a_cfg.amedas_log
        else: # target == "g"
            targetpath = a_cfg.graphs_path
        #targetpath = targetpath.replace(a_cfg.replace_target_year,entry_year).replace(a_cfg.replace_target_month,entry_month)
        targetpath = targetpath.replace(a_cfg.replace_target_year,entry_year).replace(a_cfg.replace_target_month,entry_month).replace(a_cfg.replace_target_areacode,areacode)
        #print(f"\n Target path = {targetpath} \n target date = {target_datetime} \n")
    
        return targetpath
    else:
        return "ERROR: target not supported!!! use either 'g' for graph or 'l' for log path"


# Request weather data from created URL and put the JSON result, if valid, on a dictionary
def requestWeatherData( target_datetime = "", area_code = 0 ):
    # check the date & time parameter first
    if( isinstance(target_datetime, dt.datetime) ):
        req_url = createRequestUrlFromDatetime(target_datetime)
    else:
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
        print(f"The area code -> {area_code} and its type {type(area_code)}")
        if( area_code in raw_data ):
            area_weather_info = raw_data[area_code]
        else:
            area_weather_info = "NAN"
            
    return area_weather_info


# add the response to a JSON file having all the data we collect from AMEDAS
def addWeatherValueEntry( datapoint, debugprint = False, area_code = 0, entry_datetime = "" ):
    #check if datapoint is a dict type
    if( type(datapoint) is not dict ): return False
    #form the path to the log where the entry must be saved
    entry_log = buildPathFromDate( target_datetime = entry_datetime, target = "l", areacode = area_code )
    # create the directory if required
    os.makedirs( os.path.dirname(entry_log), exist_ok = True )
    #Get data from file
    try:
        if( os.path.exists(entry_log) ):
            #Open file in read only mode only
            tempfile = open(entry_log, 'r')
            tempdata = json.load(tempfile)
            tempfile.close()
            if( debugprint == True) : print(f"Reading data from file {entry_log} \n")
        else:
            tempdata = {}
            if( debugprint == True) : print(f"New file will be created at {entry_log} \n")
    except ValueError as e:
        if( debugprint == True) : print(f"Error: {e}\n")
        if( debugprint == True) : print(f"File {entry_log} was empty \n creating new entry...\n")
        tempdata = {}
    except IOError:
        print(f"Unexpected error: {sys.exc_info()[0:2]}")

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
            if( debugprint == True) :print(f"'Added the datapoint {datapoint_full} to the key {entry_date_key} \n")
        else:
            #if not available, add new date key and add datapoint
            tempdata.update({entry_date_key:datapoint_full})
            # consider checking if value for that time is already in the list or not
            if( debugprint == True) : print(f"Created the key {entry_date_key} and added the datapoint {datapoint_full} \n")
        #finally, re-write json file
        tempfile = open(entry_log,'w')
        json.dump(tempdata, tempfile, sort_keys=True)
        if( debugprint == True) : print(f"Re-wrote data to file {entry_log} \n")
        tempfile.close()
        return True
    else:
        if( debugprint == True) : print(f"Error: entry_datetime format is not valid -> {entry_datetime}")
        return False

    
# to make my life easier... just put the request and add entry functions together ;)    
def requestAndStoreWeatherInfo( target_datetime = "", area_code = 0, debugprint = True ):
    res = False
    #just in case... check the params and create some values if required
    if( not isinstance(target_datetime, dt.datetime) ): target_datetime = dt.datetime.now()
    if( not area_code ): area_code = a_cfg.area_code
    # Request the data from the server
    weather_data = requestWeatherData( target_datetime, area_code )
    if( debugprint == True) : print(f"Got data {weather_data}")
    #now check if the result is valid or not
    if( weather_data ):
        # Storage with debug mode... will call it on a cron-job and keep a log
        res = addWeatherValueEntry( weather_data, debugprint, area_code, target_datetime )
        if( debugprint == True) : print(f"Got data for the area {area_code} at @ ({target_datetime}) = {res}")
    else:
        if( debugprint == True) : print(f"Error! not able to get data for the area {area_code} at @ ({target_datetime}) = {res}")
    return res

#----EOF--------------------------------------------------------
