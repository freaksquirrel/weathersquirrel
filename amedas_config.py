# -*- coding: utf-8 -*-
import os.path

## URL and request format related definitions
url_format = "https://www.jma.go.jp/bosai/amedas/data/map/YYYYMMDDHHMM00.json"  # Format of the URL time  -> YYYYMMDDHHMMSS
replace_target = "YYYYMMDDHHMM"
area_code = '40201'    #I use "Mito-shi" as default (Note about area codes: you can find the area code you want in the full JSON response ;) )
area_name = 'Mito-shi (JPN)'

## Path and filenames for amedas weather data
### ----------
# getcwd() does not work as expected when using the script via cronjob since the cronjob's working directory is not the script directory
# use the aux_path and iofiles_path combo is you need to set a very specific path
#aux_path = "<Set the absolute path that you want to use>"
#iofiles_path = os.path.join(aux_path, "datafiles/YYYY/MM")
iofiles_path = os.path.join(os.path.os.getcwd(), "datafiles/YYYY/MM")
### ----------
amedas_fname  = 'YYYYMM_amedas_vals.json'
amedas_log  = os.path.join(iofiles_path, amedas_fname)
replace_target_year="YYYY"
replace_target_month="MM"

## Path and filenames for graphs
### ----------
# getcwd() does not work as expected when using the script via cronjob since the cronjob's working directory is not the script directory
#aux_path = "<Set the absolute path that you want to use>"
#graphs_path = os.path.join(aux_path, "graphs/YYYY/MM")
graphs_path = os.path.join(os.path.os.getcwd(), "graphs/YYYY/MM")
### ----------
graphs_file_ext = '.png'
graph_generic_fname = 'graph_scatter_amedas_'
graph_comp_fname = 'comp_'

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

graph_amedas_dic = {"temp":['Temperature','Temp [C]', 'temp_'],
                    "humidity":['Humidity','Humidity [%]', 'humidity_'],
                    "snow":['Snow','Snow [mm?]', 'snow_'],
                    "weather":['Weather','???', 'weather_'],
                    "sun10m":['Sunlight per Hour (prev 10 min)','Sun time / 1hr', 'sunper10min_'],
                    "sun1h":['Sunlight per Hour (prev 1 hour)','Sun time / 1hr', 'sunperhour_'],
                    "precipitation10m":['Precipitation (prev 10min)','Precipitation [mm]','precipitacion10min_'],
                    "precipitation1h":['Precipitation (prev 1 hr)','Precipitation [mm]','precipitacion1h_'],
                    "precipitation3h":['Precipitation (prev 3 hr)','Precipitation [mm]','precipitacion3h_'],
                    "precipitation24h":['Precipitation (prev 24hr)','Precipitation [mm]','precipitacion24h_'],
                    "windDirection":['Wind direction', '16 directions','windirection_'],
                    "wind":['Wind','Wind [m/s]','wind_'] }
