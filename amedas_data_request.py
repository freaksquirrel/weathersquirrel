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
    parser.add_argument("--plot_temp", action='store_true', help="Plot temperature values and store somewhere...")
    parser.add_argument("--plot_hum", action='store_true', help="Plot humidity values and store somewhere...")
    parser.add_argument("--plot_rain", action='store_true', help="Plot precipitation values and store somewhere...")
    parser.add_argument("--plot_wind", action='store_true', help="Plot wind values and store somewhere...")
    parser.add_argument("--plot_temphum", action='store_true', help="Plot temperatur/humidity values and store somewhere...")
    parser.add_argument("--plot_vs_temp", action='store_true', help="temporary for test..")
    parser.add_argument("--plot", default = '', help="use the name of the value for plotting")
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
        area_code = args.area
    else:
        area_code = a_cfg.area_code

    if args.p:
        weather_data = a_fnc.requestWeatherData()
        #check if datapoint is valid
        if( weather_data ):
            print('What data -> {}'. format(weather_data))
        else:
            print('error... did not receive the kind of results I was expecting')
            
    elif args.batch:
        target_datetime = dt.datetime.now() - dt.timedelta(hours = 1)
        for minute in range(6):
            query_datetime = dt.datetime.strptime(target_datetime.strftime('%Y%m%d%H'+str(minute)+'0'), '%Y%m%d%H%M')
            print('Time {} and code {}'. format(query_datetime, a_cfg.area_code))
            res = a_fnc.requestAndStoreWeatherInfo( query_datetime, a_cfg.area_code )
    elif args.plot_temp:
        target_date = dt.datetime.now().strftime('%Y-%m-%d')
        check_date = (dt.datetime.now() - dt.timedelta(hours = 1)).strftime('%Y-%m-%d')
        #plot a scatter graph of the temperature values from a Amedas Json file
        plotres = a_plt_fnc.plotAmedasSingleScatter( data_fname=a_cfg.amedas_log, val_name='temp', date_key=target_date, plot_save_path=a_cfg.graphs_path )
        print('Plot result was: {}   ({})'.format(plotres, dt.datetime.now().strftime('%Y-%m-%d %H:%M')))
        if( not target_date == check_date):
            plotres = a_plt_fnc.plotAmedasSingleScatter( data_fname=a_cfg.amedas_log, val_name='temp', date_key=check_date, plot_save_path=a_cfg.graphs_path )
            print('Plot result (prev day) was: {}   ({})'.format(plotres, dt.datetime.now().strftime('%Y-%m-%d %H:%M')))
    elif args.plot_hum:
        target_date = dt.datetime.now().strftime('%Y-%m-%d')
        check_date = (dt.datetime.now() - dt.timedelta(hours = 1)).strftime('%Y-%m-%d')
        #plot a scatter graph of the humidity values from a Amedas Json file
        plotres = a_plt_fnc.plotAmedasSingleScatter( data_fname=a_cfg.amedas_log, val_name='humidity', date_key=target_date, plot_save_path=a_cfg.graphs_path )
        print('Plot result was: {}   ({})'.format(plotres, dt.datetime.now().strftime('%Y-%m-%d %H:%M')))
        if( not target_date == check_date):
            plotres = a_plt_fnc.plotAmedasSingleScatter( data_fname=a_cfg.amedas_log, val_name='humidity', date_key=check_date, plot_save_path=a_cfg.graphs_path )
            print('Plot result (prev day) was: {}   ({})'.format(plotres, dt.datetime.now().strftime('%Y-%m-%d %H:%M')))
    elif args.plot_temphum:
        target_date = dt.datetime.now().strftime('%Y-%m-%d')
        check_date = (dt.datetime.now() - dt.timedelta(hours = 1)).strftime('%Y-%m-%d')
        #plot a scatter graph of the temperature/humidity values from a Amedas Json file
        plotres = a_plt_fnc.plotAmedasTempHumiScatter(data_fname=a_cfg.amedas_log, plot_save_path=a_cfg.graphs_path)
        print('Plot result was: {}   ({})'.format(plotres, dt.datetime.now().strftime('%Y-%m-%d %H:%M')))
        if( not target_date == check_date):
            plotres = a_plt_fnc.plotAmedasTempHumiScatter(data_fname=a_cfg.amedas_log, date_key=check_date, plot_save_path=a_cfg.graphs_path)
            print('Plot result (prev day) was: {}   ({})'.format(plotres, dt.datetime.now().strftime('%Y-%m-%d %H:%M')))
    elif args.plot_rain:
        target_date = dt.datetime.now().strftime('%Y-%m-%d')
        check_date = (dt.datetime.now() - dt.timedelta(hours = 1)).strftime('%Y-%m-%d')
        #plot a scatter graph of the precipitation values from a Amedas Json file
        plotres = a_plt_fnc.plotAmedasSingleScatter( data_fname=a_cfg.amedas_log, val_name='precipitation1h', date_key=target_date, plot_save_path=a_cfg.graphs_path )
        print('Plot result was: {}   ({})'.format(plotres, dt.datetime.now().strftime('%Y-%m-%d %H:%M')))
        if( not target_date == check_date):
            plotres = a_plt_fnc.plotAmedasSingleScatter( data_fname=a_cfg.amedas_log, val_name='precipitation1h', date_key=check_date, plot_save_path=a_cfg.graphs_path )
            print('Plot result (prev day) was: {}   ({})'.format(plotres, dt.datetime.now().strftime('%Y-%m-%d %H:%M')))
    elif args.plot_wind:
        target_date = dt.datetime.now().strftime('%Y-%m-%d')
        check_date = (dt.datetime.now() - dt.timedelta(hours = 1)).strftime('%Y-%m-%d')
        #plot a scatter graph of the wind values from a Amedas Json file
        plotres = a_plt_fnc.plotAmedasSingleScatter( data_fname=a_cfg.amedas_log, val_name='wind', date_key=target_date, plot_save_path=a_cfg.graphs_path )
        print('Plot result was: {}   ({})'.format(plotres, dt.datetime.now().strftime('%Y-%m-%d %H:%M')))
        if( not target_date == check_date):
            plotres = a_plt_fnc.plotAmedasSingleScatter( data_fname=a_cfg.amedas_log, val_name='wind', date_key=check_date, plot_save_path=a_cfg.graphs_path )
            print('Plot result (prev day) was: {}   ({})'.format(plotres, dt.datetime.now().strftime('%Y-%m-%d %H:%M')))
    elif args.plot:
        target_date = dt.datetime.now().strftime('%Y-%m-%d')
        check_date = (dt.datetime.now() - dt.timedelta(hours = 1)).strftime('%Y-%m-%d')
        #plot a scatter graph of the wind values from a Amedas Json file
        plotres = a_plt_fnc.plotAmedasSingleScatter( data_fname=a_cfg.amedas_log, val_name=args.plot, date_key=target_date, plot_save_path=a_cfg.graphs_path )
        print('Plot result was: {}   ({})'.format(plotres, dt.datetime.now().strftime('%Y-%m-%d %H:%M')))
        if( not target_date == check_date):
            plotres = a_plt_fnc.plotAmedasSingleScatter( data_fname=a_cfg.amedas_log, val_name=args.plot, date_key=check_date, plot_save_path=a_cfg.graphs_path )
            print('Plot result (prev day) was: {}   ({})'.format(plotres, dt.datetime.now().strftime('%Y-%m-%d %H:%M')))
    elif args.plot_vs_temp:
        #lst_date = dt.datetime.now().strftime('%Y-%m-%d')
        lst_date = (dt.datetime.now() - dt.timedelta(days = 1)).strftime('%Y-%m-%d')  #yesterday
        prv_date = (dt.datetime.now() - dt.timedelta(days = 8)).strftime('%Y-%m-%d')  #1 week ago
        #plot a comparison scatter graph of the temperature values from a Amedas Json file
        # Temperature
        plotres = a_plt_fnc.plotAmedasCompareScatter_2dates( data_fname=a_cfg.amedas_log, val_name='temp', date_key_prv=prv_date, date_key_lst=lst_date, plot_save_path=a_cfg.graphs_path )
        print(f"Plot result for temp was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
        # Humidity
        plotres = a_plt_fnc.plotAmedasCompareScatter_2dates( data_fname=a_cfg.amedas_log, val_name='humidity', date_key_prv=prv_date, date_key_lst=lst_date, plot_save_path=a_cfg.graphs_path )
        print(f"Plot result for himidity was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
        # Wind
        plotres = a_plt_fnc.plotAmedasCompareScatter_2dates( data_fname=a_cfg.amedas_log, val_name='wind', date_key_prv=prv_date, date_key_lst=lst_date, plot_save_path=a_cfg.graphs_path )
        print(f"Plot result wind was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
        # Rain
        plotres = a_plt_fnc.plotAmedasCompareScatter_2dates( data_fname=a_cfg.amedas_log, val_name='precipitation1h', date_key_prv=prv_date, date_key_lst=lst_date, plot_save_path=a_cfg.graphs_path )
        print(f"Plot result for rain was: {plotres}   ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
    else:
        weather_data = a_fnc.request_weather_data()
        if( weather_data ):
            # Storage with debug mode... will call it on a cron-job and keep a log
            res = a_fnc.addWeatherValEntry( weather_data, True, area_code, entry_date, entry_time )
            print('Got data for the area {} at @ ({} {}) = {}'.format(area_code, entry_date, entry_time, res))
        else:
            print('Error! not able to get data for the area {} at @ ({} {}) = {}'.format(area_code, entry_date, entry_time, res))


if __name__ == '__main__':
    sys.exit(main())
