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
import amedas_funcs as a_fnc


# Composite scatter plot of a given information (e.g. rain, temperature, wind, etc)
def plotAmedasCompositeScatter(data_fname='', val_name_A='', val_name_B='', date_key='', plot_save_path='./', area_code = 0 ):
    #if there is no file given or value_name not valid, then do nothing
    if( not data_fname or val_name_A not in a_cfg.graph_amedas_dic or val_name_B not in a_cfg.graph_amedas_dic ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')
    if( plot_save_path == './'): plot_save_path = a_fnc.buildPathFromDate( target_datetime = date_key, target = "g", area_code = area_code  )
    
    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_generic_fname + a_cfg.graph_amedas_dic[val_name_A][2] + 'And_' + a_cfg.graph_amedas_dic[val_name_B][2] + date_key + a_cfg.graphs_file_ext)
    # create the directory if required
    os.makedirs( os.path.dirname(plot_fname), exist_ok = True )
    
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print(f"Date ({date_key}) does not exists in the JSON file. Graph will not be created.")
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    
    yAxis  = [value[area_code][val_name_A][0] for key, value in todayvals_sorted.items()]
    yAxis2 = [value[area_code][val_name_B][0] for key, value in todayvals_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on construction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    plt.title(f"{a_cfg.graph_amedas_dic[val_name_A][0]} / {a_cfg.graph_amedas_dic[val_name_B][0]} @ {a_cfg.area_info[area_code]['name']} {date_key}")
    ax.set_xlabel('Time [%H]')
    ax.set_ylabel(a_cfg.graph_amedas_dic[val_name_A][1], color='limegreen')
    if(val_name_A == "humidity"): ax.set_ylim([0,(100)])     ## TEMP solution, TODO: Set limit based on the category?
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #create the second axis
    ax2 = ax.twinx()
    ax2.plot(xAxis,yAxis2, color='deepskyblue', marker='o')
    #plt.grid(True)
    plt.grid(color = 'deepskyblue', linestyle = '--', linewidth = 0.5)
    ax2.set_ylabel(a_cfg.graph_amedas_dic[val_name_B][1], color='deepskyblue')
    if(val_name_B == "humidity"): ax2.set_ylim([0,(100)])     ## TEMP solution, TODO: Set limit based on the category?
    ax2.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    plt.xlim([0,(24)])
    
    #save the plot!
    plt.savefig(plot_fname)

    return True


# Simple scatter plot of a given information (e.g. rain, temperature, wind, etc)
def plotAmedasSingleScatter(data_fname='', val_name='', date_key='', plot_save_path='./', area_code = 0 ):
    #if there is no file given or value_name not valid, then do nothing
    if( not data_fname or val_name not in a_cfg.graph_amedas_dic ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')
    if( plot_save_path == './'): plot_save_path = a_fnc.buildPathFromDate( target_datetime = date_key, target = "g", area_code = area_code )
       
    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_generic_fname + a_cfg.graph_amedas_dic[val_name][2] + date_key + a_cfg.graphs_file_ext)
    # create the directory if required
    os.makedirs( os.path.dirname(plot_fname), exist_ok = True )
    
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print(f"Date ({date_key}) does not exists in the JSON file. Graph will not be created.")
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[area_code][val_name][0] for key, value in todayvals_sorted.items()]
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
    plt.title(f"{a_cfg.graph_amedas_dic[val_name][0]} @ {a_cfg.area_info[area_code]['name']} {date_key}")
    plt.xlabel('Time [%H]')
    plt.ylabel(a_cfg.graph_amedas_dic[val_name][1])
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)
    
    return True


# Scatter plot comparing values of a given information for 2 different dates (e.g. rain, temperature, wind, etc, for today and 1 week ago)
# if dates are not given, the function defaults to today and yesterday data comparison
def plotAmedasCompareScatter_2dates( val_name='', date_key_prv='', date_key_lst='', plot_save_path='./', area_code = 0 ):
    #if value_name is not valid, then do nothing
    if( val_name not in a_cfg.graph_amedas_dic ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key_prv and not date_key_lst ):
        date_key_lst = dt.date.today().strftime('%Y-%m-%d')
        date_key_prv = (dt.date.today() - dt.timedelta(days = 1)).strftime('%Y-%m-%d')
    elif( not date_key_prv ):
        date_key_prv =  (dt.datetime.strptime( date_key_lst, '%Y-%m-%d') - dt.timedelta(days = 1) ).strftime('%Y-%m-%d')
    elif( not date_key_lst ):
        date_key_lst =  (dt.datetime.strptime( date_key_prv, '%Y-%m-%d') + dt.timedelta(days = 1) ).strftime('%Y-%m-%d')
    if( isinstance(date_key_prv, dt.datetime) ): date_key_prv = date_key_prv.strftime('%Y-%m-%d')
    if( isinstance(date_key_lst, dt.datetime) ): date_key_lst = date_key_lst.strftime('%Y-%m-%d')
    if( not area_code ): area_code = a_cfg.area_code_def
    
    data_fname_prv = a_fnc.buildPathFromDate( target_datetime = date_key_prv, target = "l", area_code = area_code )
    data_fname_lst = a_fnc.buildPathFromDate( target_datetime = date_key_lst, target = "l", area_code = area_code )
    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_generic_fname + a_cfg.graph_amedas_dic[val_name][2] + a_cfg.graph_comp_fname + date_key_prv + 'vs' + date_key_lst + a_cfg.graphs_file_ext)
    # create the directory if required
    os.makedirs( os.path.dirname(plot_fname), exist_ok = True )
    
    #get the data from the json file
    if( data_fname_prv == data_fname_lst ):
        data_fname = data_fname_prv
        allvals = json.load(open(data_fname, 'r'))
        if date_key_prv not in allvals.keys():
            print(f"Date ({date_key_prv}) does not exists in the JSON file. Graph will not be created.")
            return False
        if date_key_lst not in allvals.keys():
            print(f"Date ({date_key_lst}) does not exists in the JSON file. Graph will not be created.")
            return False
    
        vals_prv = allvals[date_key_prv]
        vals_lst = allvals[date_key_lst]
    else:
        allvals_prv = json.load(open(data_fname_prv, 'r'))
        if date_key_prv not in allvals_prv.keys():
            print(f"Date ({date_key_prv}) does not exists in the JSON file. Graph will not be created.")
            return False
        allvals_lst = json.load(open(data_fname_lst, 'r'))
        if date_key_lst not in allvals_lst.keys():
            print(f"Date ({date_key_lst}) does not exists in the JSON file. Graph will not be created.")
            return False
    
        vals_prv = allvals_prv[date_key_prv]
        vals_lst = allvals_lst[date_key_lst]

    vals_prv_sorted = ordDict(sorted(vals_prv.items()))
    vals_lst_sorted = ordDict(sorted(vals_lst.items()))
    yAxis_prv  = [value[area_code][val_name][0] for key, value in vals_prv_sorted.items()]
    yAxis_lst  = [value[area_code][val_name][0] for key, value in vals_lst_sorted.items()]
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
    plt.plot(xAxis_lst, yAxis_lst, color='deepskyblue', marker='v', label = date_key_lst)
    plt.grid(True)
    plt.xlim([0,(24)])
    plt.title(f"{a_cfg.graph_amedas_dic[val_name][0]} @ {a_cfg.area_info[area_code]['name']} {date_key_prv} vs {date_key_lst}")
    plt.xlabel('Time [%H]')
    plt.legend()
    plt.ylabel(a_cfg.graph_amedas_dic[val_name][1])
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)
    
    return True


# Scatter plot comparing values of a given information for 2 different areas (e.g. rain, temperature, wind, etc, for Mito and Tokyo)
def plotAmedasCompareScatter_2areas( val_name='', area_code_A='', area_code_B='', date_key='', plot_save_path='./' ):
    # if value_name is not valid, then do nothing
    if( val_name not in a_cfg.graph_amedas_dic ): return False
    # if the any of the area codes are not valid, then do nothing
    if( area_code_A not in a_cfg.area_info or area_code_B not in a_cfg.area_info ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ):
        date_key = dt.date.today().strftime('%Y-%m-%d')
    if( isinstance(date_key, dt.datetime) ): date_key = date_key.strftime('%Y-%m-%d')
    
    data_fname_areaA = a_fnc.buildPathFromDate( target_datetime = date_key, target = "l", area_code = area_code_A )
    data_fname_areaB = a_fnc.buildPathFromDate( target_datetime = date_key, target = "l", area_code = area_code_B )
    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, a_cfg.graph_generic_fname + a_cfg.graph_amedas_dic[val_name][2] + a_cfg.area_info[area_code_A]['short_name'] + 'VS' + a_cfg.area_info[area_code_B]['short_name'] + '_' + date_key + a_cfg.graphs_file_ext)
    # create the directory if required
    os.makedirs( os.path.dirname(plot_fname), exist_ok = True )
    
    #get the data from the json file
    if( data_fname_areaA == data_fname_areaB ):
        data_fname = data_fname_areaA
        allvals = json.load(open(data_fname, 'r'))
        if date_key not in allvals.keys():
            print(f"Date ({date_key}) does not exists in the JSON file for area {area_code_A}. Graph will not be created.")
            return False
    
        vals_areaA = allvals[date_key]
        vals_areaB = allvals[date_key]
    else:
        allvals_areaA = json.load(open(data_fname_areaA, 'r'))
        if date_key not in allvals_areaA.keys():
            print(f"Date ({date_key}) does not exists in the JSON file for area {area_code_A}. Graph will not be created.")
            return False
        allvals_areaB = json.load(open(data_fname_areaB, 'r'))
        if date_key not in allvals_areaB.keys():
            print(f"Date ({date_key}) does not exists in the JSON file for area {area_code_B}. Graph will not be created.")
            return False
    
        vals_areaA = allvals_areaA[date_key]
        vals_areaB = allvals_areaB[date_key]

    vals_areaA_sorted = ordDict(sorted(vals_areaA.items()))
    vals_areaB_sorted = ordDict(sorted(vals_areaB.items()))
    yAxis_areaA  = [value[area_code_A][val_name][0] for key, value in vals_areaA_sorted.items()]
    yAxis_areaB  = [value[area_code_B][val_name][0] for key, value in vals_areaB_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis_areaA = [0]*len(yAxis_areaA)
    for (index, (key, value)) in enumerate(vals_areaA_sorted.items()):
        xAxis_areaA[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    xAxis_areaB = [0]*len(yAxis_areaB)
    for (index, (key, value)) in enumerate(vals_areaB_sorted.items()):
        xAxis_areaB[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on construction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis_areaA, yAxis_areaA, color='limegreen', marker='v',   label = a_cfg.area_info[area_code_A]['name'])
    plt.plot(xAxis_areaB, yAxis_areaB, color='deepskyblue', marker='v', label = a_cfg.area_info[area_code_B]['name'])
    plt.grid(True)
    plt.xlim([0,(24)])
    plt.title(f"{a_cfg.graph_amedas_dic[val_name][0]} @ {date_key} - {a_cfg.area_info[area_code_A]['name']} vs {a_cfg.area_info[area_code_B]['name']}")
    plt.xlabel('Time [%H]')
    plt.legend()
    plt.ylabel(a_cfg.graph_amedas_dic[val_name][1])
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)
    
    return True


# Scatter plot comparing values of a given information for all areas (e.g. rain, temperature, wind, etc.)
def plotAmedasCompareScatter_Allareas( val_name='', date_key='', plot_save_path='./' ):
    # if value_name is not valid, then do nothing
    if( val_name not in a_cfg.graph_amedas_dic ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ):
        date_key = dt.date.today().strftime('%Y-%m-%d')
    if( isinstance(date_key, dt.datetime) ): date_key = date_key.strftime('%Y-%m-%d')

    data_fname_areas = {}
    for areacd in a_cfg.area_info :
        if( areacd == 'common' ): continue
        data_fname_area = a_fnc.buildPathFromDate( target_datetime = date_key, target = "l", area_code = areacd )
        data_fname_areas[areacd] = data_fname_area

    if( data_fname_areas ):
        # List not empty
        plot_fname = os.path.join(plot_save_path, a_cfg.graph_generic_fname + a_cfg.graph_amedas_dic[val_name][2] + a_cfg.graph_comp_fname + 'AllAreasVS' + '_' + date_key + a_cfg.graphs_file_ext)
        # create the directory if required
        os.makedirs( os.path.dirname(plot_fname), exist_ok = True )

        # get the data from the json files and set the plot and format the plot
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 5))
        for data_areacd, data_jsonpath in data_fname_areas.items() :
            allvals_area = json.load(open(data_jsonpath, 'r'))
            if date_key not in allvals_area.keys():
                print(f"Date ({date_key}) does not exists in the JSON file for area {data_areacd}. Graph will not be created.")
                return False
            vals_area = allvals_area[date_key]
            vals_area_sorted = ordDict(sorted(vals_area.items()))
            # set the Y axis
            yAxis_area = [value[data_areacd][val_name][0] for key, value in vals_area_sorted.items()]
            # set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
            xAxis_area = [0]*len(yAxis_area)
            for (index, (key, value)) in enumerate(vals_area_sorted.items()):
                xAxis_area[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)
            # plot the values for the current area
            plt.plot(xAxis_area, yAxis_area, color=a_cfg.area_info[data_areacd]['color'], marker=a_cfg.area_info[data_areacd]['marker'], label=a_cfg.area_info[data_areacd]['name'])

        plt.grid(True)
        plt.xlim([0,(24)])
        plt.title(f"{a_cfg.graph_amedas_dic[val_name][0]} @ {date_key}")
        plt.xlabel('Time [%H]')
        plt.legend()
        plt.ylabel(a_cfg.graph_amedas_dic[val_name][1])
        if(val_name == "humidity"): plt.ylim([0,(100)])     ## TEMP solution, TODO: Set limit based on the category?
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
        #save the plot!
        plt.savefig(plot_fname)

        return True
    else:
        #Nothing to do here
        print("No data!")
        return False

#----EOF--------------------------------------------------------
