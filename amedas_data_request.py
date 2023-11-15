# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import argparse
import sys
import os.path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import datetime as dt
import json
import amedas_config as a_cfg
import amedas_funcs as a_fnc
import amedas_plot_funcs as a_plt_fnc


def main():
    parser = argparse.ArgumentParser( description="Get weather data from AMEADAS api...",  )
    parser.add_argument("-p", action='store_true', help="Print out values on terminal (does not store values)")
    parser.add_argument("-a", "--area", type = int, default = 0, help="Specific area to request weather data")
    parser.add_argument("--date", help="Specific date to request weather data [YYYY-MM-DD format date]")
    parser.add_argument("--time", help="Specific time to request weather data [HH time format]")
    parser.add_argument("-b", "--batch", action='store_true', help="Get each 10 min weather values for last hour")
    parser.add_argument("--batch_datetime", help="Specific date to request weather data in batch [YYYY-MM-DD-HH format datetime]")
    parser.add_argument("--plot_comp_week", action='store_true', help="Plot graphs that compare the weather of [1 day ago] vs [1 week ago].")
    parser.add_argument("--plot_comp_dates", nargs=2, metavar=('date_A','date_B'), help="Plot graphs that compare the weather of 2 different dates")
    parser.add_argument("--plot_comp_areas", nargs=2, metavar=('area_sn_A','area_sn_B'), help="Plot graphs that compare the weather of 2 different areas (ref. by short name)")
    parser.add_argument("--plot", default = '', help="Plot a category from Amedas Log file, use the name of the value for plotting (e.g. 'wind' , 'precipitation1h')")
    parser.add_argument("--plot_composite", nargs=2, metavar=('value_A','value_B'), help="Plot graph comparing 2 categories.")
    args = parser.parse_args()

    # set now() - 10 minutes as default datetime 
    datetime_now_adjusted = dt.datetime.now() - dt.timedelta(minutes = 10)
    
    # set the date for the weather data query
    if args.date:
        try:
            entry_date = dt.datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            entry_date = datetime_now_adjusted
            print(f"Warning: Invalid date argument, will use date from now() - 10 minutes instead -> {entry_date.strftime('%Y-%m-%d')}")
    else:
        # use now() - 10 minutes as default
        entry_date = datetime_now_adjusted

    # set the time for the weather data query
    if args.time:
        try:
            entry_time = dt.datetime.strptime(args.time, '%H:%M')
        except ValueError:
            entry_time = datetime_now_adjusted
            print(f"Warning: Invalid date argument, will use time from now() - 10 minutes instead -> {entry_time.strftime('%H:%M')}")
    else:
        # use now() - 10 minutes as default
        entry_time = datetime_now_adjusted

    # set the entry datetime based on the arguments or the default values
    entry_datetime = entry_datetime = entry_date.strftime('%Y%m%d') + entry_time.strftime('%H%M')
    print(f"Entry datetime -> {entry_datetime}")
    
    # set the region for the weather data query
    if args.area != 0 :
        area_code = str(args.area)
    else:
        area_code = a_cfg.area_code_def

    if args.batch_datetime:
        try:
            batch_datetime = dt.datetime.strptime(args.batch_datetime, '%Y-%m-%d-%H')
        except ValueError:
            batch_datetime = ""
            print(f"Warning: Invalid datetime argument for batch, will use default values")
    else:
        batch_datetime = ""

    # Now, select ONLY one of the rest of the options
    if args.p:
        # get data from a given area at a given date/time
        weather_data = a_fnc.requestWeatherData( target_datetime = entry_datetime, area_code = area_code, request_mode = 'a' )
        # check if resulting data point is valid
        if( weather_data ):
            print(f"Acquired data -> {weather_data}")
        else:
            print("Error... did not receive the kind of results I was expecting")
    elif args.batch:
        if( batch_datetime ):
            # set the target date/time for the batch process based on the user given argument
            target_datetime = batch_datetime
        else:            
            # set the target date/time for the batch process (1 hour earlier than now() ) *default
            target_datetime = dt.datetime.now() - dt.timedelta(hours = 1)
            
        for minute in range(6):
            query_datetime = dt.datetime.strptime(target_datetime.strftime('%Y%m%d%H'+str(minute)+'0'), '%Y%m%d%H%M')
            if( args.area != 0 ):
                print(f"Time {query_datetime} and code {area_code}")
                res = a_fnc.requestAndStoreSingleWeatherInfo( query_datetime, area_code )
            else:
                print(f"Time {query_datetime} for multiple area query")
                res = a_fnc.requestAndStoreWeatherInfo( query_datetime )
                print(f"Successfully retrieved data for {res} areas")
    elif args.plot:
        # Plot a single scatter graph of a certain category values from a Amedas Json file
        # By default, use a 1-hour before now() setting to avoid blank graphs at the beggining of the day
        check_date = (dt.datetime.now() - dt.timedelta(hours = 1)).strftime('%Y-%m-%d')
        logfile = a_fnc.buildPathFromDate( target_datetime = check_date, target = "l", area_code = area_code )
        graph_path = a_fnc.buildPathFromDate( target_datetime = check_date, target = "g", area_code = area_code )
        plotres = a_plt_fnc.plotAmedasSingleScatter( data_fname=logfile, val_name=args.plot, date_key=check_date, plot_save_path=graph_path, area_code = area_code )
        print(f"Plot result for {args.plot} from ({check_date}) was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
    elif args.plot_composite:
        try:
            # try to get the values from the arguments
            value_A, value_B = args.plot_composite
        except ValueError as e:
            print(f"Error: {e} -> you need to set 2 values, no more, no less. Try something like --plot_composite temp humidity")
            return ''
        # Plot a comparison scatter graph of values from 2 categories from a Amedas Json file
        # By default, use a 1-hour before now() setting to avoid blank graphs at the beggining of the day
        check_date = (dt.datetime.now() - dt.timedelta(hours = 1)).strftime('%Y-%m-%d')
        logfile = a_fnc.buildPathFromDate( target_datetime = check_date, target = "l", area_code = area_code )
        graph_path = a_fnc.buildPathFromDate( target_datetime = check_date, target = "g", area_code = area_code )
        plotres = a_plt_fnc.plotAmedasCompositeScatter( data_fname=logfile, val_name_A=value_A, val_name_B=value_B, date_key=check_date, plot_save_path=graph_path, area_code = area_code )
        print(f"Plot result for {args.plot_composite} from ({check_date}) was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
    elif args.plot_comp_week:
        lst_date = (dt.datetime.now() - dt.timedelta(days = 1)).strftime('%Y-%m-%d')  #yesterday
        prv_date = (dt.datetime.now() - dt.timedelta(days = 8)).strftime('%Y-%m-%d')  #1 week ago
        graph_path = a_fnc.buildPathFromDate( target_datetime = lst_date, target = "g", area_code = area_code )
        #plot a comparison scatter graph of the temperature values from a Amedas Json file
        # Temperature
        plotres = a_plt_fnc.plotAmedasCompareScatter_2dates( val_name='temp', date_key_prv=prv_date, date_key_lst=lst_date, plot_save_path=graph_path, area_code = area_code )
        print(f"Plot result for temp was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
        # Humidity
        plotres = a_plt_fnc.plotAmedasCompareScatter_2dates( val_name='humidity', date_key_prv=prv_date, date_key_lst=lst_date, plot_save_path=graph_path, area_code = area_code )
        print(f"Plot result for himidity was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
        # Wind
        plotres = a_plt_fnc.plotAmedasCompareScatter_2dates( val_name='wind', date_key_prv=prv_date, date_key_lst=lst_date, plot_save_path=graph_path, area_code = area_code )
        print(f"Plot result wind was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
        # Rain
        plotres = a_plt_fnc.plotAmedasCompareScatter_2dates( val_name='precipitation1h', date_key_prv=prv_date, date_key_lst=lst_date, plot_save_path=graph_path, area_code = area_code )
        print(f"Plot result for rain was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
    elif args.plot_comp_dates:
        try:
            # try to get the values from the arguments
            date_A, date_B = args.plot_comp_dates
            # and convert them to datetime format
            lst_date = dt.datetime.strptime( date_A, '%Y-%m-%d')
            prv_date = dt.datetime.strptime( date_B, '%Y-%m-%d')
        except ValueError as e:
            print(f"Error: {e} -> Try something like --plot_comp_dates 2023-11-02 2023-11-01")
            return ''
        graph_path = a_fnc.buildPathFromDate( target_datetime = lst_date, target = "g", area_code = area_code )
        #plot a comparison scatter graph of the temperature values from a Amedas Json file
        # Temperature
        plotres = a_plt_fnc.plotAmedasCompareScatter_2dates( val_name='temp', date_key_prv=prv_date, date_key_lst=lst_date, plot_save_path=graph_path, area_code = area_code )
        print(f"Plot result for temp was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
        # Humidity
        plotres = a_plt_fnc.plotAmedasCompareScatter_2dates( val_name='humidity', date_key_prv=prv_date, date_key_lst=lst_date, plot_save_path=graph_path, area_code = area_code )
        print(f"Plot result for himidity was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
        # Wind
        plotres = a_plt_fnc.plotAmedasCompareScatter_2dates( val_name='wind', date_key_prv=prv_date, date_key_lst=lst_date, plot_save_path=graph_path, area_code = area_code )
        print(f"Plot result wind was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
        # Rain
        plotres = a_plt_fnc.plotAmedasCompareScatter_2dates( val_name='precipitation1h', date_key_prv=prv_date, date_key_lst=lst_date, plot_save_path=graph_path, area_code = area_code )
        print(f"Plot result for rain was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
    elif args.plot_comp_areas:
        try:
            # try to get the values from the arguments
            area_sn_A, area_sn_B = args.plot_comp_areas
            area_A, area_B = ['','']
            # and check that they are in the data that we have registered
            for areacd_check in a_cfg.area_info :
                if( areacd_check == 'common' ): continue
                if( area_sn_A in list(a_cfg.area_info[areacd_check].values()) ): area_A = areacd_check
                if( area_sn_B in list(a_cfg.area_info[areacd_check].values()) ): area_B = areacd_check
            if( not area_A or not area_B ):
                print(f"Error: Either or both area's short names is not valid... Try something like --plot_comp_areas mito tokyo")
                return ''
        except ValueError as e:
            print(f"Error: {e} -> Try something like --plot_comp_areas mito tokyo")
            return ''
        # By default, use a 1-hour before now() setting to avoid blank graphs at the beggining of the day
        check_date = (dt.datetime.now() - dt.timedelta(hours = 1)).strftime('%Y-%m-%d')
        graph_path = a_fnc.buildPathFromDate( target_datetime = check_date, target = "g", area_code = 'common' )
        #plot a comparison scatter graph of the temperature values from a Amedas Json file
        # Temperature
        plotres = a_plt_fnc.plotAmedasCompareScatter_2areas( val_name='temp', area_code_A=area_A, area_code_B=area_B, date_key=check_date, plot_save_path=graph_path )
        print(f"Plot result for temp was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
        # Humidity
        plotres = a_plt_fnc.plotAmedasCompareScatter_2areas( val_name='humidity', area_code_A=area_A, area_code_B=area_B, date_key=check_date, plot_save_path=graph_path )
        print(f"Plot result for himidity was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
        # Wind
        plotres = a_plt_fnc.plotAmedasCompareScatter_2areas( val_name='wind', area_code_A=area_A, area_code_B=area_B, date_key=check_date, plot_save_path=graph_path )
        print(f"Plot result wind was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
        # Rain
        plotres = a_plt_fnc.plotAmedasCompareScatter_2areas( val_name='precipitation1h', area_code_A=area_A, area_code_B=area_B, date_key=check_date, plot_save_path=graph_path )
        print(f"Plot result for rain was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
    else:
        # Default mode
        res = a_fnc.requestAndStoreWeatherInfo()


if __name__ == '__main__':
    sys.exit(main())

#----EOF--------------------------------------------------------
