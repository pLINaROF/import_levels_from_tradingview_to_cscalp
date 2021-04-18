# import_levels_from_tradingview_to_cscalp

# Общая информация
Программа получает названия всех фьючерсов с сайта binance.com через api, для каждого из них с сайта tradingview.com получает уровни (поддерживаются горизонтальные уровни и горизонтальные лучи) для фьючерса и/или спота (можно включить или выключить в конфиге(tradingview_levels.ini, параметры import_spot_levels, import_futures_levels) и записывает уровни в настройки стаканов cscalp.
Запись уровней необходимо осуществлять на закрытом приводе. Для этого в программе реализована пауза.
Авторизация на tradingview.com осуществляется через куки и jwt, примерно раз в неделю их нужно будет обновлять в файле tradingview_levels.ini.


# Заполнение tradingview_levels.ini
Для заполнения tradingview_levels.ini нужно авторизоваться на tradingview.com, открыть любой график, открыть инструменты разработчика (Ctrl + Shift + J или F12), перейти во вкладку Network, в списке котировок нажать на любую другую монету. В Network появится запрос sources?chart_id. Нажимаем на него. Начинаем собирать данные для tradingview_levels.ini.

chart - раздел General - Request URL - нужна часть между layout и sources (без слешей)
cookie - раздел Request Headers - cookie
user_agent - раздел Request Headers - user_agent
chart_id - раздел Query String Parameters - chart_id
jwt - раздел Query String Parameters - jwt

Вставляем собранные данные в tradingview_levels.ini, сохраняем

Параметры import_spot_levels, import_futures_levels отвечают за парсинг уровней для спота и фьючерса соответсвенно (True - парсим, False - не парсим (я использую только import_futures_levels так быстрее)).

