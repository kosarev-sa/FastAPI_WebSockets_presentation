from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def send_exclusive_data(ws: WebSocket, data_to_send, data_lst: list):
    # Отправка уникальных сообщений, которых ещё нет в списке
    if data_to_send['message'] not in data_lst:
        # Отправка с использованием JSON
        await ws.send_json(data_to_send)
        data_lst.append(data_to_send['message'])
    else:
        await ws.send_json({"number": '', "message": "Не повторяйся!"})


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    # Ожидаем подключение клиента
    await ws.accept()

    # Список отправленных сообщений
    idioms = []
    # Анонсируем выводимые данные
    await ws.send_json({"number": 'N', "message": "Цитата"})

    try:
        while True:
            # Ожидаем сообщения клиента
            data = await ws.receive_json()
            print('INFO:    ', data, type(data))
            # Формируем и отпраляем порядковый номер и сообщение
            data_to_send = {"number": len(idioms) + 1, "message": data['message']}
            await send_exclusive_data(ws, data_to_send, idioms)

    # Обрабатываем разрыв соединения
    except WebSocketDisconnect:
        print(f"INFO:     ('{ws.client.host}', {ws.client.port}) - "
              f"\"WebSocket /ws\" [disconnected]")


if __name__ == "__main__":
    import uvicorn
    # Запуск UVICORN-server с параметрами
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=False)
