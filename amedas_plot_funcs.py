# -*- coding: utf-8 -*-

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

def plotAmedasTempScatter(data_fname='', date_key='', plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')

    #create a file name for the plot
    #plot_fname = os.path.join(plot_save_path, 'graph_scatter_amedas_temp_' + date_key + '.png')
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_temp_fname + date_key + a_cfg.graphs_file_ext)
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print('Date ({}) does not exists in the JSON file. Graph will not be created.'.format(date_key))
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[a_cfg.area_code]['temp'][0] for key, value in todayvals_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on cunstruction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    #plt.ylim([0,(40)])
    plt.title('Temperature @ {}'.format(date_key))
    plt.xlabel('Time [%H]')
    plt.ylabel('Temp [Celcius]')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)

    return True

def plotAmedasHumidityScatter(data_fname='', date_key='', plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')

    #create a file name for the plot
    #plot_fname = os.path.join(plot_save_path, 'graph_scatter_amedas_humidity_' + date_key + '.png')
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_hum_fname + date_key + a_cfg.graphs_file_ext)
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print('Date ({}) does not exists in the JSON file. Graph will not be created.'.format(date_key))
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[a_cfg.area_code]['humidity'][0] for key, value in todayvals_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on cunstruction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    #plt.ylim([0,(40)])
    plt.title('Temperature @ {}'.format(date_key))
    plt.xlabel('Time [%H]')
    plt.ylabel('Humidity [%]')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)

    return True

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
        print('Date ({}) does not exists in the JSON file. Graph will not be created.'.format(date_key))
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[a_cfg.area_code]['temp'][0] for key, value in todayvals_sorted.items()]
    yAxis2 = [value[a_cfg.area_code]['humidity'][0] for key, value in todayvals_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on cunstruction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.title('Temperature / Humidity @ {}'.format(date_key))
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
    #plot_fname = os.path.join(plot_save_path, 'graph_scatter_amedas_humidity_' + date_key + '.png')
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_rain_fname + date_key + a_cfg.graphs_file_ext)
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print('Date ({}) does not exists in the JSON file. Graph will not be created.'.format(date_key))
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

    #Format the plot   (this part is still on cunstruction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    #plt.ylim([0,(40)])
    plt.title('{} @ {}'.format(title_str, date_key))
    plt.xlabel('Time [%H]')
    #plt.ylabel('Precipitation [mm]')
    plt.ylabel(label_str)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)

    return True


def plotAmedasWindScatter(data_fname='', date_key='', plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')
    
    #create a file name for the plot
    #plot_fname = os.path.join(plot_save_path, 'graph_scatter_amedas_humidity_' + date_key + '.png')
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_wind_fname + date_key + a_cfg.graphs_file_ext)
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print('Date ({}) does not exists in the JSON file. Graph will not be created.'.format(date_key))
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

    #Format the plot   (this part is still on cunstruction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    #plt.ylim([0,(40)])
    plt.title('{} @ {}'.format(title_str, date_key))
    plt.xlabel('Time [%H]')
    plt.ylabel(label_str)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)

    return True


def plotAmedasGenericScatter(data_fname='', val_name='', date_key='', plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')

    #"precipitation10m": [0.0, 0]
    #"precipitation1h": [0.0, 0]
    #"precipitation24h": [0.0, 0]
    #"precipitation3h": [0.0, 0]
    
    #create a file name for the plot
    #plot_fname = os.path.join(plot_save_path, 'graph_scatter_amedas_humidity_' + date_key + '.png')
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_generic_fname + date_key + a_cfg.graphs_file_ext)
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print('Date ({}) does not exists in the JSON file. Graph will not be created.'.format(date_key))
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[a_cfg.area_code][val_name][0] for key, value in todayvals_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on cunstruction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    #plt.ylim([0,(40)])
    plt.title('{} @ {}'.format(val_name, date_key))
    plt.xlabel('Time [%H]')
    plt.ylabel('Generic [?]')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)

    return True

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
        print('Date ({}) does not exists in the JSON file. Graph will not be created.'.format(date_key))
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[a_cfg.area_code][val_name][0] for key, value in todayvals_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on cunstruction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    #plt.ylim([0,(40)])
    plt.title('{} @ {}'.format(a_cfg.graph_amedas_dic[val_name][0], date_key))
    plt.xlabel('Time [%H]')
    plt.ylabel(a_cfg.graph_amedas_dic[val_name][1])
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)
    
    return True
