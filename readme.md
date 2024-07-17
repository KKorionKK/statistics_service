**Statistics service**

В качестве базы данных был выбран Redis. Сервер поднят на aiohttp, использована библиотека jsonrpcserver

**Использование**

Настройки вносятся в *prod.env* в папке *app/common/global_configs*. Выбор активных рутов производится в *app/common/settings.py*

**Пример запроса**
```
curl -X POST http://127.0.0.1:PORT/ENDPOINT -d '{
    "jsonrpc": "2.0",
    "method": "init_stats",
    "params": ["cars, frees"],
    "id": 1
}'
```
