from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:
    '''Класс - ядро серверной программы'''
    # Список отправленных сообщений
    idioms = []

    def __init__(self):
        # Список подключенных сокетов
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        # Соединение с сервером
        if len(self.active_connections) >= 1:
            # Запрещаем подключение другим пользователям,
            # но оставляем возможность для расширения программы в будущем
            await ws.accept()
            await ws.close(4000)
        else:
            await ws.accept()
            self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        # Отключение и удаление объекта WebSocket из списка
        self.active_connections.remove(ws)
        # Обнуляем список отправленных сообщений
        self.idioms = []

    async def broadcast(self, data: dict):
        # Отправка сообщений с использованием JSON
        for connection in self.active_connections:
            await connection.send_json(data)

    async def send_exclusive_data(self, data_to_send):
        # Отправка уникальных сообщений, которых ещё нет в списке
        if data_to_send['message'] not in self.idioms:
            await self.broadcast(data_to_send)
            self.idioms.append(data_to_send['message'])
        else:
            if self.idioms.index(data_to_send['message']) != 0:
                await self.broadcast({"number": '', "message": "Не повторяйся!"})


# Объект класса ConnectionManager
manager = ConnectionManager()


# Устанавливаем соединение
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    # Ожидаем подключение клиента
    await manager.connect(ws)

    # Анонсируем выводимые данные
    data_to_send = {"number": 'N', "message": "Цитата"}
    await manager.send_exclusive_data(data_to_send)

    try:
        while True:
            # Ожидаем сообщения клиента
            data = await ws.receive_json()
            print('INFO: ', data, type(data))

            # Формируем и отпраляем порядковый номер и сообщение
            data_to_send = {"number": len(manager.idioms), "message": data['message']}
            await manager.send_exclusive_data(data_to_send)

    # Обрабатываем разрыв соединения
    except WebSocketDisconnect:
        manager.disconnect(ws)
        await manager.broadcast({"number": '', "message": "Выход"})


if __name__ == "__main__":
    import uvicorn
    # Запуск UVICORN-server с параметрами
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=False)
