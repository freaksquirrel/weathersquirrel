# -*- coding: utf-8 -*-
import os.path

## URL and request format related definitions
url_format = "https://www.jma.go.jp/bosai/amedas/data/map/YYYYMMDDHHMM00.json"  # Format of the URL time  -> YYYYMMDDHHMMSS
replace_target = "YYYYMMDDHHMM"
## Area related information ('common' is used for graphs like those related to value comparison between different areas)
##            CODE      Area name          Area short name         Area name in japanese
area_info = {'40201': {'name':'Mito'   , 'short_name':'mito'   , 'japanese_name':'水戸（ミト）'},
             '44132': {'name':'Tokyo'  , 'short_name':'tokyo'  , 'japanese_name':'東京（トウキョウ）'},
             '14163': {'name':'Sapporo', 'short_name':'sapporo', 'japanese_name':'札幌（サッポロ）'},
             '62078': {'name':'Osaka'  , 'short_name':'osaka'  , 'japanese_name':'大阪(オオサカ)'},
             '82182': {'name':'Fukuoka', 'short_name':'fukuoka', 'japanese_name':'福岡（フクオカ）'},
             '91197': {'name':'Naha'   , 'short_name':'naha'   , 'japanese_name':'那覇（ナハ）'},
             'common':{'name':'_'      , 'short_name':'comm'   , 'japanese_name':'_'}                 }
area_code_def = '40201'    #I use "Mito" as default but you can change it to whatever area you want
## Note about area codes: you can find the area code you want in the full JSON response ;)
##                        also check this for more info -> https://www.jma.go.jp/bosai/map.html#5/35.246/137/&elem=temp&contents=amedas&interval=60
##                        After cliking on the area you want to get info from, you can get the codes by looking at the URL and get the value after the var 'amdno'
##                        example url for Mito -> https://www.jma.go.jp/bosai/amedas/#area_type=offices&area_code=080000&amdno=40201&format=table1h&elems=53614
##                        info also available here https://www.jma.go.jp/jma/kishou/know/amedas/ame_master.pdf    and here  https://www.jma.go.jp/jma/kishou/know/amedas/kaisetsu.html

## Path and filenames for amedas weather data
replace_target_year="YYYY"
replace_target_month="MM"
replace_target_areacode="ACODE"
### ----------
## getcwd() does not work as expected when using the script via cronjob since the cronjob's working directory is not the script directory
## use the aux_path and iofiles_path combo is you need to set a very specific path
#aux_path = "<Set the absolute path that you want to use>"
#iofiles_path = os.path.join(aux_path, "datafiles/ACODE/YYYY/MM")
iofiles_path = os.path.join(os.path.os.getcwd(), "datafiles/ACODE/YYYY/MM")
### ----------
amedas_fname  = 'YYYYMM_amedas_vals.json'
amedas_log  = os.path.join(iofiles_path, amedas_fname)

## Path and filenames for graphs
### ----------
## getcwd() does not work as expected when using the script via cronjob since the cronjob's working directory is not the script directory
#aux_path = "<Set the absolute path that you want to use>"
#graphs_path = os.path.join(aux_path, "graphs/ACODE/YYYY/MM")
graphs_path = os.path.join(os.path.os.getcwd(), "graphs/ACODE/YYYY/MM")
### ----------
graphs_file_ext = '.png'
graph_generic_fname = 'graph_scatter_amedas_'
graph_comp_fname = 'comp_'
# date comparison related info (yesterday and 8 days ago setting)
ndays_timedelta_lst = 1
ndays_timedelta_prv = 8
## info for plots   value (json format)       Name                           Axis title          filename
graph_amedas_dic = {"temp":             ['Temperature'                     ,'Temp [°C]'          ,'01_temp_'              ],
                    "humidity":         ['Humidity'                        ,'Humidity [%]'       ,'02_humidity_'          ],
                    "snow":             ['Snow'                            ,'Snow [cm]'          ,'06_snow_'              ],
                    "pressure":         ['Sea level pressure'              ,'Sea level pressure' ,'05_pressure_'          ],
                    "sun10m":           ['Sunlight per Hour (prev 10 min)' ,'Sun time / 1hr'     ,'07_sunper10min_'       ],
                    "sun1h":            ['Sunlight per Hour (prev 1 hour)' ,'Sun time / 1hr'     ,'07_sunperhour_'        ],
                    "precipitation10m": ['Precipitation (prev 10min)'      ,'Precipitation [mm]' ,'03_precipitacion10min_'],
                    "precipitation1h":  ['Precipitation (prev 1 hr)'       ,'Precipitation [mm]' ,'03_precipitacion1h_'   ],
                    "precipitation3h":  ['Precipitation (prev 3 hr)'       ,'Precipitation [mm]' ,'03_precipitacion3h_'   ],
                    "precipitation24h": ['Precipitation (prev 24hr)'       ,'Precipitation [mm]' ,'03_precipitacion24h_'  ],
                    "windDirection":    ['Wind direction'                  ,'16 directions'      ,'04_windirection_'      ],
                    "wind":             ['Wind'                            ,'Wind [m/s]'         ,'04_wind_'              ] }

## Wind directions 北、北北東、北東、東北東、東、東南東、南東、南南東、南、南南西、南西、西南西、西、西北西、北西、北北西
## will do something with that data later on... maybe...
