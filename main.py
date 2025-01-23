import websocket
import json
import pandas as pd
import matplotlib.pyplot as plt
import ssl
import certifi
import websocket

# Указание пути к сертификатам
ssl_context = ssl.create_default_context(cafile=certifi.where())

# URL WebSocket для Deribit
url = 'wss://www.deribit.com/ws/api/v2/'

# Функция для обработки данных и построения графика
def on_message(ws, message):
    data = json.loads(message)
    
    # Проверим, содержит ли сообщение результат
    if 'result' in data:
        instruments = data['result']
        df = pd.DataFrame(instruments)
        
        # Выведем первые несколько строк, чтобы проверить структуру данных
        print(df.head())

        # Предположим, что в данных есть поле 'implied_volatility' (если оно есть)
        if 'implied_volatility' in df.columns:
            volatility = df['implied_volatility']
        
            # Построение графика
            plt.figure(figsize=(10, 6))
            plt.plot(df['instrument_name'], volatility)
            plt.title('Implied Volatility Over Time')
            plt.xlabel('Instrument')
            plt.ylabel('Implied Volatility')
            
            # Сохранение графика
            plt.savefig('volatility_plot.png')
            
            # Показать график
            plt.show()
        else:
            print("Столбец 'implied_volatility' не найден в данных.")
    else:
        print("Результат не найден в сообщении.")

# Функция для открытия WebSocket-соединения
def on_open(ws):
    # Подписка на канал данных инструментов
    subscribe_message = {
        "jsonrpc": "2.0",
        "method": "public/get_historical_volatility",
        "params": {
            "channels": ["deribit_price_index.BTC-USD.raw"]
        },
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))

# Обработчик ошибок
def on_error(ws, error):
    print(f"Ошибка: {error}")

# Обработчик закрытия соединения
def on_close(ws, close_status_code, close_msg):
    print("Соединение закрыто")

ws = websocket.WebSocketApp(
    'wss://www.deribit.com/ws/api/v2/',
    on_message=on_message,
    on_open=on_open,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever(sslopt={"context": ssl_context})