# FastAPI_WebSockets_presentation

Задача: 
С использованием fastapi необходимо создать веб-страницу состоящую из
1. Формы с текстовым полем
2. Списка сообщений, пронумерованных с 1

Страница подключается к серверу по WebSocket.
С помощью формы вы можете отправить сообщение на сервер, где оно будет принято и добавлен порядковый номер этого сообщения.
Далее сообщение с порядковым номером отправляется на страницу и отображается в списке.

При перезагрузке страницы данные о номерации теряются и начинается с 1.

Страница должна быть динамической, обрабатывать все действия без перезагрузки, 
т.е. при отправке сообщения на сервер через вебсокет страница не должна перезагружаться.  
Взаимодействие с сервером по вебсокет нужно реализовать с использованием JSON. Формат и именование полей могут быть любые.
___________________________________________________________________________________________________________________________

How to install:
pip install -r requirements.txt

How to run:
cd ./server
uvicorn main:app --reload
(or any method to run the script main.py)

Open in a browser ./client/index.html

