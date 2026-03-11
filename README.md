# API Monitor

Сервис проверяет доступность API и сохраняет метрики.
Данные пишутся в PostgreSQL. Grafana показывает графики.

Проверка выполняется каждые **30 секунд**.

---

# Что делает сервис

1. Отправляет запрос к API.
2. Измеряет время ответа.
3. Сохраняет результат в базу.
4. Grafana строит графики.

Метрики:

* тип эндпоинта
* HTTP статус
* время ответа
* успешность запроса
* ошибка (если была)
* время проверки

---

# Стек

* Python
* PostgreSQL
* Grafana
* Docker

---


# Запуск

1. Создать `.env` по аналогии `.env.tmpl`

2. Запустить сервисы

```
docker compose up --build
```

---

# Доступ

Grafana:

```
http://localhost:3000
```

логин:

```
admin
admin
```

PostgreSQL (с хоста):

```
localhost:5439
```

---

# Подключение базы в Grafana

Datasource → PostgreSQL

```
Host: db:5439
Database: monitoring
User: 
Password: 
SSL: disable
```

---


# Как добавить новый API

Добавить запись в `app/endpoints.py`.

Пример:

```
ENDPOINTS = [
  {
    "endpoint_type": "dadata_party_lookup",
    "url": "...",
    "payload": {...}
  }
]
