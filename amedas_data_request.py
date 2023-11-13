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
    parser.add_argument("-a", "--area", type = int, default = 0, help="Specific area to request weather data")
    parser.add_argument("--date",  help="YYYY-MM-DD format date")
    parser.add_argument("--time",  help="HH time format")
    parser.add_argument("--datetime",  help="YYYY-MM-DD-HH-MM format")
    parser.add_argument("-p", action='store_true', help="Print out values on terminal")
    parser.add_argument("--batch", action='store_true', help="Get each 10 min weather values for last hour")
    parser.add_argument("--plot_comp_week", action='store_true', help="Plot graphs that compare the weather of [1 day ago] vs [1 week ago].")
    parser.add_argument("--plot_comp_dates", nargs=2, metavar=('date_A','date_B'), help="Plot graphs that compare the weather of 2 different dates")
    parser.add_argument("--plot", default = '', help="Plot a category from Amedas Log file, use the name of the value for plotting (e.g. 'wind' , 'precipitation1h')")
    parser.add_argument("--plot_composite", nargs=2, metavar=('value_A','value_B'), help="Plot graph comparing 2 categories.")
    args = parser.parse_args()

    # set the date for the weather data query
    if args.date:
        try:
            entry_date = dt.datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            entry_date = dt.datetime.now()
    else:
        entry_date = dt.datetime.now()

    # set the time for the weather data query
    if args.time:
        try:
            entry_time = dt.datetime.strptime(args.time, '%H:%M')
        except ValueError:
            entry_time = dt.datetime.now()
    else:
        entry_time = dt.datetime.now()

    # set the region for the weather data query
    if args.area != 0 :
        area_code = str(args.area)
    else:
        area_code = a_cfg.area_code

    if args.p:
        weather_data = a_fnc.requestWeatherData()
        #check if datapoint is valid
        if( weather_data ):
            print(f"Acquired data -> {weather_data}")
        else:
            print("Error... did not receive the kind of results I was expecting")
    elif args.batch:
        target_datetime = dt.datetime.now() - dt.timedelta(hours = 1)
        for minute in range(6):
            query_datetime = dt.datetime.strptime(target_datetime.strftime('%Y%m%d%H'+str(minute)+'0'), '%Y%m%d%H%M')
            print(f"Time {query_datetime} and code {area_code}")
            res = a_fnc.requestAndStoreWeatherInfo( query_datetime, area_code )
    elif args.plot:
        # Plot a single scatter graph of a certain category values from a Amedas Json file
        # By default, use a 1-hour before now() setting to avoid blank graphs at the beggining of the day
        check_date = (dt.datetime.now() - dt.timedelta(hours = 1)).strftime('%Y-%m-%d')
        logfile = a_fnc.buildPathFromDate( target_datetime = check_date, target = "l", areacode = area_code )
        graph_path = a_fnc.buildPathFromDate( target_datetime = check_date, target = "g", areacode = area_code )
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
        logfile = a_fnc.buildPathFromDate( target_datetime = check_date, target = "l", areacode = area_code )
        graph_path = a_fnc.buildPathFromDate( target_datetime = check_date, target = "g", areacode = area_code )
        plotres = a_plt_fnc.plotAmedasCompositeScatter( data_fname=logfile, val_name_A=value_A, val_name_B=value_B, date_key=check_date, plot_save_path=graph_path, area_code = area_code )
        print(f"Plot result for {args.plot_composite} from ({check_date}) was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
    elif args.plot_comp_week:
        lst_date = (dt.datetime.now() - dt.timedelta(days = 1)).strftime('%Y-%m-%d')  #yesterday
        prv_date = (dt.datetime.now() - dt.timedelta(days = 8)).strftime('%Y-%m-%d')  #1 week ago
        graph_path = a_fnc.buildPathFromDate( target_datetime = lst_date, target = "g", areacode = area_code )
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
        graph_path = a_fnc.buildPathFromDate( target_datetime = lst_date, target = "g", areacode = area_code )
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
    else:
        # Default mode
        res = a_fnc.requestAndStoreWeatherInfo()


if __name__ == '__main__':
    sys.exit(main())

#----EOF--------------------------------------------------------
