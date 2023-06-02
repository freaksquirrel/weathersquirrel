# -*- coding: utf-8 -*-
import os.path

## URL and request format related definitions
url_format = "https://www.jma.go.jp/bosai/amedas/data/map/YYYYMMDDHHMM00.json"  # Format of the URL time  -> YYYYMMDDHHMMSS
replace_target = "YYYYMMDDHHMM"
area_code = '40201'    #I use "Mito-shi" as default (Note about area codes: you can find the area code you want in the full JSON response ;) )
area_name = 'Mito-shi (JPN)'

## Path and filenames for amedas weather data
#iofiles_path = '<path to root folder of this app>/datafiles'
iofiles_path = os.path.join(os.path.os.getcwd(), "datafiles")
amedas_fname  = 'amedas_vals.json'
amedas_log  = os.path.join(iofiles_path, amedas_fname)

## Path and filenames for graphs
#graphs_path = '<path to root folder of this app>/graphs'
graphs_path = os.path.join(os.path.os.getcwd(), "graphs")
graphs_file_ext = '.png'
graph_temp_fname = 'graph_scatter_amedas_temp_'
graph_hum_fname = 'graph_scatter_amedas_humidity_'
graph_rain_fname = 'graph_scatter_amedas_precipitacion_'
graph_wind_fname = 'graph_scatter_amedas_wind_'
graph_generic_fname = 'graph_scatter_amedas_generic_'
graph_temphum_fname = 'graph_scatter_amedas_temp-humi_'

graph_title_label = {"temp":['Temperature','Temp [C]'],
                     "humidity":['Humidity','Humidity [%]'],
                     "snow":['Snow','Snow [mm?]'],
                     "weather":['Weather','???'],
                     "sun10m":['Sunlight per Hour (prev 10 min)','Sun time / 1hr'],
                     "sun1h":['Sunlight per Hour (prev 1 hour)','Sun time / 1hr'],
                     "precipitation10m":['Precipitation (prev 10min)','Precipitation [mm]'],
                     "precipitation1h":['Precipitation (prev 1 hr)','Precipitation [mm]'],
                     "precipitation3h":['Precipitation (prev 3 hr)','Precipitation [mm]'],
                     "precipitation24h":['Precipitation (prev 24hr)','Precipitation [mm]'],
                     "windDirection":['Wind direction', '16 directions'],
                     "wind":['Wind','Wind [m/s]'] }

graph_amedas_dic = {"temp":['Temperature','Temp [C]', 'graph_scatter_amedas_temp_'],
                    "humidity":['Humidity','Humidity [%]', 'graph_scatter_amedas_humidity_'],
                    "snow":['Snow','Snow [mm?]', 'graph_scatter_amedas_snow_'],
                    "weather":['Weather','???', 'graph_scatter_amedas_weather_'],
                    "sun10m":['Sunlight per Hour (prev 10 min)','Sun time / 1hr', 'graph_scatter_amedas_sunper10min_'],
                    "sun1h":['Sunlight per Hour (prev 1 hour)','Sun time / 1hr', 'graph_scatter_amedas_sunperhour_'],
                    "precipitation10m":['Precipitation (prev 10min)','Precipitation [mm]','graph_scatter_amedas_precipitacion10min_'],
                    "precipitation1h":['Precipitation (prev 1 hr)','Precipitation [mm]','graph_scatter_amedas_precipitacion_'],
                    "precipitation3h":['Precipitation (prev 3 hr)','Precipitation [mm]','graph_scatter_amedas_precipitacion3h_'],
                    "precipitation24h":['Precipitation (prev 24hr)','Precipitation [mm]','graph_scatter_amedas_precipitacion24h_'],
                    "windDirection":['Wind direction', '16 directions','graph_scatter_amedas_windirection_'],
                    "wind":['Wind','Wind [m/s]','graph_scatter_amedas_wind_'] }
