import xml.etree.ElementTree as ET
import os
import configparser

config = configparser.ConfigParser()
config.read("tradingview_levels.ini")
file_name_pref = config["def"]["file_name_pref"]


def update_value_in_tmp(file, iter, value):
    tmp = ET.ElementTree(file=file)
    for user_levels in tmp.iter(iter):
        user_levels.set('Value', f'{value}')
    tmp.write(file, "UTF-8")


for file in os.listdir():
    if file_name_pref in file:
        try:
            update_value_in_tmp(file, 'UserLevels', '')
            update_value_in_tmp(file, 'UserSignalPriceLevels', '')
        except:
            pass

input('Чистка уровней завершена')

# C:\Users\WINDOWS_USER_NAME\AppData\Roaming\CScalp\Visualizer
# C:\Users\WINDOWS_USER_NAME\AppData\Roaming\CScalp\Visualizer\mvs_cs
# pyinstaller levels_cleaner.py --onefile
