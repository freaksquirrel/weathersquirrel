# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import datetime as dt
import os.path
import json
from collections import OrderedDict as ordDict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import amedas_config as a_cfg

# Simple temperature scatter (may remove this later as I made a generic function for all kind of info) 
def plotAmedasTempScatter(data_fname='', date_key='', plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')

    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_temp_fname + date_key + a_cfg.graphs_file_ext)
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print(f"Date ({date_key}) does not exists in the JSON file. Graph will not be created.")
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[a_cfg.area_code]['temp'][0] for key, value in todayvals_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on construction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    plt.title(f"Temperature @ {a_cfg.area_name} {date_key}")
    plt.xlabel('Time [%H]')
    plt.ylabel('Temp [Celcius]')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)

    return True


# Simple humidity scatter (may remove this later as I made a generic function for all kind of info) 
def plotAmedasHumidityScatter(data_fname='', date_key='', plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')

    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_hum_fname + date_key + a_cfg.graphs_file_ext)
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print(f"Date ({date_key}) does not exists in the JSON file. Graph will not be created.")
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[a_cfg.area_code]['humidity'][0] for key, value in todayvals_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on construction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    plt.title(f"Temperature @ {a_cfg.area_name} {date_key}")
    plt.xlabel('Time [%H]')
    plt.ylabel('Humidity [%]')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)

    return True


# Temp and humidity scatter
def plotAmedasTempHumiScatter(data_fname='', date_key='', plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')

    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_temphum_fname + date_key + a_cfg.graphs_file_ext)
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print(f"Date ({date_key}) does not exists in the JSON file. Graph will not be created.")
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[a_cfg.area_code]['temp'][0] for key, value in todayvals_sorted.items()]
    yAxis2 = [value[a_cfg.area_code]['humidity'][0] for key, value in todayvals_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on construction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.title(f"Temperature / Humidity @ {a_cfg.area_name} {date_key}")
    ax.set_xlabel('Time [%H]')
    ax.set_ylabel('Temp [Celcius]', color='limegreen')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #create the second axis
    ax2 = ax.twinx()
    ax2.plot(xAxis,yAxis2, color='mediumblue', marker='o')
    #plt.grid(True)
    plt.grid(color = 'blue', linestyle = '--', linewidth = 0.5)
    ax2.set_ylabel('Humidity [%]',color='blue')
    ax2.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    plt.xlim([0,(24)])
    plt.ylim([0,(100)])
    
    #save the plot!
    plt.savefig(plot_fname)

    return True


# Simple Rain scatter (may remove this later as I made a generic function for all kind of info) 
def plotAmedasRainScatter(data_fname='', date_key='', detailed = False, plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')

    #"precipitation10m": [0.0, 0]
    #"precipitation1h": [0.0, 0]
    #"precipitation24h": [0.0, 0]
    #"precipitation3h": [0.0, 0]
    
    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_rain_fname + date_key + a_cfg.graphs_file_ext)
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print(f"Date ({date_key}) does not exists in the JSON file. Graph will not be created.")
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    if( detailed ) :
        yAxis  = [value[a_cfg.area_code]['precipitation10m'][0] for key, value in todayvals_sorted.items()]
        title_str = a_cfg.graph_title_label['precipitation10m'][0]     #'10 min'
        label_str = a_cfg.graph_title_label['precipitation10m'][1]     #mm
    else:
        yAxis  = [value[a_cfg.area_code]['precipitation1h'][0] for key, value in todayvals_sorted.items()]
        title_str = a_cfg.graph_title_label['precipitation1h'][0]     #'hour'
        label_str = a_cfg.graph_title_label['precipitation1h'][1]     #mm
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on construction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    plt.title(f"{title_str} @ {a_cfg.area_name} {date_key}")
    plt.xlabel('Time [%H]')
    plt.ylabel(label_str)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)

    return True


# Simple Wind scatter (may remove this later as I made a generic function for all kind of info) 
def plotAmedasWindScatter(data_fname='', date_key='', plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')
    
    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_wind_fname + date_key + a_cfg.graphs_file_ext)
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print(f"Date ({date_key}) does not exists in the JSON file. Graph will not be created.")
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[a_cfg.area_code]['wind'][0] for key, value in todayvals_sorted.items()]
    title_str = a_cfg.graph_title_label['wind'][0]
    label_str = a_cfg.graph_title_label['wind'][1]     #m/s
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on construction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    plt.title(f"{title_str} @ {a_cfg.area_name} {date_key}")
    plt.xlabel('Time [%H]')
    plt.ylabel(label_str)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)

    return True

# Simple generic scatter (may remove this later as I made a generic function for all kind of info) 
def plotAmedasGenericScatter(data_fname='', val_name='', date_key='', plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')
    
    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_generic_fname + date_key + a_cfg.graphs_file_ext)
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print(f"Date ({date_key}) does not exists in the JSON file. Graph will not be created.")
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[a_cfg.area_code][val_name][0] for key, value in todayvals_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on construction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    plt.title(f"{val_name} @ {a_cfg.area_name} {date_key}.")
    plt.xlabel('Time [%H]')
    plt.ylabel('Generic [?]')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)

    return True


# Simple scatter plot of a given information (e.g. rain, temperature, wind, etc)
def plotAmedasSingleScatter(data_fname='', val_name='', date_key='', plot_save_path='./'):
    #if there is no file given or value_name not valid, then do nothing
    if( not data_fname or val_name not in a_cfg.graph_amedas_dic ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')
    
    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_amedas_dic[val_name][2] + date_key + a_cfg.graphs_file_ext)
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print(f"Date ({date_key}) does not exists in the JSON file. Graph will not be created.")
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[a_cfg.area_code][val_name][0] for key, value in todayvals_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on construction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    plt.title(f"{a_cfg.graph_amedas_dic[val_name][0]} @ {a_cfg.area_name} {date_key}")
    plt.xlabel('Time [%H]')
    plt.ylabel(a_cfg.graph_amedas_dic[val_name][1])
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)
    
    return True


# Scatter plot comparing values of a given information for 2 different dates (e.g. rain, temperature, wind, etc, for today and 1 week ago)
# if dates are nmot given, the function defaults to today and yesterday data comparison
def plotAmedasCompareScatter_2dates(data_fname='', val_name='', date_key_prv='', date_key_lst='', plot_save_path='./'):
    #if there is no file given or value_name not valid, then do nothing
    if( not data_fname or val_name not in a_cfg.graph_amedas_dic ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key_prv and not date_key_lst ):
        date_key_lst = dt.date.today().strftime('%Y-%m-%d')
        date_key_prv = (dt.date.today() - dt.timedelta(days = 1)).strftime('%Y-%m-%d')
    elif( not date_key_prv ):
        date_key_prv =  (dt.datetime.strptime( date_key_lst, '%Y-%m-%d') - dt.timedelta(days = 1) ).strftime('%Y-%m-%d')
    elif( not date_key_lst ):
        date_key_lst =  (dt.datetime.strptime( date_key_prv, '%Y-%m-%d') + dt.timedelta(days = 1) ).strftime('%Y-%m-%d')
    
    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_amedas_dic[val_name][2] + a_cfg.graph_comp_fname + date_key_prv + 'vs' + date_key_lst + a_cfg.graphs_file_ext)
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key_prv not in allvals.keys():
        print(f"Date ({date_key_prv}) does not exists in the JSON file. Graph will not be created.")
        return False
    if date_key_lst not in allvals.keys():
        print(f"Date ({date_key_lst}) does not exists in the JSON file. Graph will not be created.")
        return False
    
    vals_prv = allvals[date_key_prv]
    vals_prv_sorted = ordDict(sorted(vals_prv.items()))
    vals_lst = allvals[date_key_lst]
    vals_lst_sorted = ordDict(sorted(vals_lst.items()))
    
    yAxis_prv  = [value[a_cfg.area_code][val_name][0] for key, value in vals_prv_sorted.items()]
    yAxis_lst  = [value[a_cfg.area_code][val_name][0] for key, value in vals_lst_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis_prv = [0]*len(yAxis_prv)
    for (index, (key, value)) in enumerate(vals_prv_sorted.items()):
        xAxis_prv[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    xAxis_lst = [0]*len(yAxis_lst)
    for (index, (key, value)) in enumerate(vals_lst_sorted.items()):
        xAxis_lst[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on construction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis_prv, yAxis_prv, color='limegreen', marker='v',  label = date_key_prv)
    plt.plot(xAxis_lst, yAxis_lst, color='mediumblue', marker='v', label = date_key_lst)
    plt.grid(True)
    plt.xlim([0,(24)])
    plt.title(f"{a_cfg.graph_amedas_dic[val_name][0]} @ {a_cfg.area_name} {date_key_prv} vs {date_key_lst}")
    plt.xlabel('Time [%H]')
    plt.legend()
    plt.ylabel(a_cfg.graph_amedas_dic[val_name][1])
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)
    
    return True

#----EOF--------------------------------------------------------
