# import_levels_from_tradingview_to_cscalp



# Предыстория
Уровни в стакане сильно помогают в торговле, но процесс их ручного переноса занимал много времени, поэтому было принято решение этот процесс автоматизировать.

Сейчас перенос занимает около 2 минут (включен перенос уровней только по фьючерсам, если включить спот, будет примерно в 2 раза больше).

Видео работы: https://youtu.be/5GDSrRafiCY (продемонстрирован перенос уровней по BTCUSDTPERP, но уровни были перенесены по всем монетам появившимся в окне tradingview_levels.exe)

# Как это работает?
Программа получает названия всех фьючерсов с сайта binance.com через api, для каждого из них с сайта tradingview.com получает уровни (поддерживаются горизонтальные уровни и горизонтальные лучи) для фьючерса и/или спота (можно включить или выключить в конфиге (tradingview_levels.ini, параметры import_spot_levels, import_futures_levels) и записывает уровни в настройки стаканов cscalp.

Запись уровней необходимо осуществлять на закрытом приводе. Для этого в программе реализована пауза.
Авторизация на tradingview.com осуществляется через параметры в tradingview_levels.ini, примерно раз в неделю их нужно будет обновлять в файле.

Чистка уровней осуществляется программой levels_cleaner (её использование необязательно, при запуске tradingview_levels.exe старые значения заменяются новыми). Она очищает значения уровней и сигнальных уровней во всех файлов у которых в названии есть "BINAD" (обозначение настроек стаканов для биржи Binance, можно поменять на другое значение в tradingview_levels.ini) в папке C:\Users\WINDOWS_USER_NAME\AppData\Roaming\CScalp\Visualizer\mvs_cs.

В Cscalp есть лимит на количество уровней (точное число не помню), поэтом сильно частить с уровнями в TradingView не стоит.

# Требования:
* Доступ в интернет
* Python 3.8 (при установке поставить галочку "Add Python to environment variables")
* Библиотека requests
* Созданный аккаунт в TradingView
* Установленный Cscalp

# Предостережение:
Перед началом работы ознакомьтесь с лицензией и создайте резервную копию настроек стаканов и графиков Cscalp (C:\Users\WINDOWS_USER_NAME\AppData\Roaming\CScalp\Visualizer, где WINDOWS_USER_NAME - имя пользователя Windows)

# Заполнение tradingview_levels.ini
Для заполнения tradingview_levels.ini нужно авторизоваться на tradingview.com, открыть любой график, открыть инструменты разработчика (F12 или Ctrl + Shift + J), перейти во вкладку Network, в списке котировок нажать на монету отличную от открытой. В Network появится запрос sources?chart_id. Нажимаем на него. Начинаем собирать данные для tradingview_levels.ini:

* **chart** - раздел General - Request URL - нужна часть между layout и sources (без слешей)
* **cookie** - раздел Request Headers - cookie
* **user_agent** - раздел Request Headers - user_agent
* **chart_id** - раздел Query String Parameters - chart_id
* **jwt** - раздел Query String Parameters - jwt

Значения копируем полностью без пробелов в конце и в начале.

Картинка для наглядности https://prnt.sc/11mzftx

Вставляем собранные данные в tradingview_levels.ini, сохраняем.

Параметры import_spot_levels, import_futures_levels отвечают за парсинг уровней для спота и фьючерса соответственно (True - парсим, False - не парсим (я использую только import_futures_levels, так быстрее)).

# Компиляция
Для работы программы нужно скомпилировать код.
Процесс описан здесь:
* http://toolmark.ru/kak-skompilirovat-python-prilozhenie/
* https://vc.ru/newtechaudit/122327-kompiliruem-kod-python-v-fayl-exe

Если вы не хотите компилировать код или не знаете как это сделать в репозитории есть уже упакованные в exe файлы.

Их работоспособность не гарантирована.

Файлы tradingview_levels.exe и levels_cleaner.exe нужно будет добавить в исключения антивируса (даже если вы компилировали их самостоятельно).

# Способ запуска без компиляции
Запускаем файл setup.bat (установится библиотека requests)
Перемещаем файлы tradingview_levels.ini, tradingview_levels_run.bat, tradingview_levels.py, levels_cleaner_run.bat, levels_cleaner.py в в папку с настройками стаканов Cscalp (путь:  C:\Users\WINDOWS_USER_NAME\AppData\Roaming\CScalp\Visualizer\mvs_cs, WINDOWS_USER_NAME нужно заменить на название пользователя windows (можно посмотреть в настройках или в папке C:\Users)).

Для удобства запуска можно создать ярлыки на рабочем столе для файлов (ПКМ - Отправить - Рабочий стол (создать ярлык)).

# Подготовка
Перед запуском программы нужно положить файлы tradingview_levels.exe, levels_cleaner.exe и tradingview_levels.ini в папку с настройками стаканов Cscalp (путь:  C:\Users\WINDOWS_USER_NAME\AppData\Roaming\CScalp\Visualizer\mvs_cs, WINDOWS_USER_NAME нужно заменить на название пользователя windows (можно посмотреть в настройках или в папке C:\Users)).

Для удобства запуска можно создать ярлыки на рабочем столе (ПКМ - Отправить - Рабочий стол (создать ярлык)).

# Donate
Если эта программа вам помогла, не стесняйтесь пожертвовать:
* USDT TRC20: TYvX3gNRghPo6prxVxB9G1pcuEdvCtNUM9 
* BTC: 1A4cCqEBD7U6YLtMFsmqJqZLnKS3g9bZGy
* ETH ERC20: 0xcc559ad9e92621555310d8f5e923ee7a3d914471
* BNB BEP20 (BSC): 0xcc559ad9e92621555310d8f5e923ee7a3d914471
* LTC: LU5rNY1uJEvHpUoTJ8ma6FiG6aMxgxBrim
* BCH: 1A4cCqEBD7U6YLtMFsmqJqZLnKS3g9bZGy
* DOGE: D5wo6uqCxBgtXe4xKYQAvS9jYdorfnmVkD
* XRP BEP20 (BSC): 0xcc559ad9e92621555310d8f5e923ee7a3d914471

