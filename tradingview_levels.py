import requests
import datetime
import configparser
import xml.etree.ElementTree as ET
import os


try:
    config = configparser.ConfigParser()
    config.read("tradingview_levels.ini")

    jwt = config["def"]["jwt"]
    cookie = config["def"]["cookie"]
    chart_id = config["def"]["chart_id"]
    exchange_name = config["def"]["exchange_name"]
    user_agent = config["def"]["user_agent"]
    chart = config["def"]["chart"]
    import_futures_levels = config["def"].getboolean('import_futures_levels')
    import_spot_levels = config["def"].getboolean('import_spot_levels')
except KeyError:
    input(print('Проблемы с конфигом (tradingview_levels.ini)\nПроверьте его наличие и правильность заполнения'))


def get_binance_futures_list():
    futures = requests.get('https://www.binance.com/fapi/v1/ticker/price').json()
    futures_list = []
    for f in futures:
        futures_list.append(f['symbol'])
    return futures_list


def get_tradingview_levels(exchange_name, symbol, cookie, jwt, chart_id):
    url = f"https://charts-storage.tradingview.com/charts-storage/layout/{chart}/sources?" \
          f"chart_id={chart_id}&jwt={jwt}&symbol={exchange_name}%3A{symbol}"
    headers = {'cookie': f'{cookie}', 'user-agent': f'{user_agent}'}
    response = requests.request("GET", url, headers=headers).json()
    levels_prices_list = []
    # print(response)
    if 'errorMsg' in response:
        print(response)
        input('Устраните ошибки и перезапустите')
        exit()

    try:
        for source in response['payload']['sources']:
            s = response['payload']['sources'][source]
            if s['state']['type'] in ['LineToolHorzRay', 'LineToolHorzLine']:
                levels_prices_list.append(s['state']['points'][0]['price'])
    except:
        pass
    # print(levels_prices_list)
    return symbol, levels_prices_list


def cscalp_levels_format(prices_list):
    today_date = datetime.date.today().strftime("%d.%m.%Y")
    prices_list = list(map(str, prices_list))
    prices_list_with_date = []
    for price in prices_list:
        prices_list_with_date.append(f'{price}/{today_date}')
    return ';'.join(prices_list_with_date)


def update_value_in_tmp(file, iter, value):
    tmp = ET.ElementTree(file=file)
    for user_levels in tmp.iter(iter):
        user_levels.set('Value', f'{value}')
    tmp.write(file, "UTF-8")
# update_value_in_tmp('BINAD.CCUR.AAVEUSDT_Settings_MlIav_example.tmp', 'UserLevels', '60.6/09.12.2020')


all_levels = {}
print('Получаем уровни из trading_view')

for symbol in get_binance_futures_list():
    if import_spot_levels is True:
        # spot
        symbol, levels_prices_list = get_tradingview_levels(exchange_name, symbol, cookie, jwt, chart_id)
        # print(symbol, levels_prices_list)
        print(symbol)
        all_levels[symbol] = levels_prices_list

    if import_futures_levels is True:
        # futures
        symbol, levels_prices_list = get_tradingview_levels(exchange_name, symbol + 'PERP', cookie, jwt, chart_id)
        # print(symbol, levels_prices_list)
        print(symbol)
        all_levels[symbol] = levels_prices_list


print('Уровни получены')
input('Убедитесь что cscalp отключен и нажмите Enter')
print('Записываем уровни в настройки cscalp')

for file in os.listdir():
    # print(file)
    try:
        exchange, spot_or_fut, setting_name, n = file.split('.')
        symbol_name, settings, key = setting_name.split('_')
        # print(file, cscalp_levels_format(all_levels[symbol_name]))
        if spot_or_fut == 'CCUR' and exchange_name[0:4] in exchange:
            update_value_in_tmp(file, 'UserLevels', cscalp_levels_format(all_levels[symbol_name]))
        elif spot_or_fut == 'CCUR_FUT' and exchange_name[0:4] in exchange:
            symbol_name = symbol_name + 'PERP'
            update_value_in_tmp(file, 'UserLevels', cscalp_levels_format(all_levels[symbol_name]))
    except:
        pass

input('Готово, можно запустить cscalp')

# C:\Users\WINDOWS_USER_NAME\AppData\Roaming\CScalp\Visualizer
# C:\Users\WINDOWS_USER_NAME\AppData\Roaming\CScalp\Visualizer\mvs_cs
# pyinstaller tradingview_levels.py --onefile
