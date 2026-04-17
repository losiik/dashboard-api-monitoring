# Dashboard API Monitoring

Сервис мониторит внешний API DaData, измеряет время ответа и пишет результат проверок в PostgreSQL. Дальше эти данные может забирать Grafana для графиков и алертов.

## Что есть в проекте

- `app/endpoints.py` содержит список API для мониторинга.
- `app/dadata_client.py` выполняет HTTP-запрос и собирает метрику ответа.
- `app/metrics_service.py` сохраняет метрику в БД.
- `app/scheduler.py` циклически запускает проверки с заданным интервалом.
- `main.py` применяет миграции и запускает scheduler.

Текущий сценарий мониторинга проверяет `findById/party` в DaData по ИНН.

## Как работает сервис

1. Scheduler берёт очередной endpoint из списка `ENDPOINTS`.
2. Клиент отправляет POST-запрос в DaData.
3. Сервис измеряет время ответа и формирует метрику:
   - `endpoint_type`
   - `status_code`
   - `response_time_ms`
   - `success`
   - `error`
4. Метрика сохраняется в таблицу `api_check`.
5. После этого цикл повторяется через `settings.check_interval`.

## Запуск приложения

1. Создать `.env` по аналогии с `.env.tmpl`.
2. Поднять сервисы:

```bash
docker compose up --build
```

## Доступы

Grafana:

```text
http://localhost:3000
```

Логин/пароль по умолчанию:

```text
admin
admin
```

PostgreSQL с хоста:

```text
localhost:5439
```

## Подключение PostgreSQL в Grafana

Datasource -> PostgreSQL

```text
Host: db:5439
Database: monitoring
User:
Password:
SSL: disable
```

## Как добавить новый API

Добавить новый словарь в `app/endpoints.py`.

Пример:

```python
ENDPOINTS = [
    {
        "endpoint_type": "dadata_party_lookup",
        "url": "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party",
        "payload": {"query": "7707083893"},
    }
]
```

## Unit-тесты

Тесты находятся в каталоге `tests/` и написаны на стандартном `unittest`, без реальных HTTP-запросов и без подключения к настоящей БД. Все внешние зависимости эмулируются через `unittest.mock`.

Запуск:

```bash
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Набор тест-кейсов

| Модуль                          |  Тест-кейс                                                | Что проверяет                                                                                                           |
|---------------------------------|-----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| `tests/test_dadata_client.py`   | `test_returns_success_metric_for_http_200`                | При ответе DaData `200 OK` формируется успешная метрика, а заголовок `Authorization` содержит API-ключ.                 |
| `tests/test_dadata_client.py`   | `test_marks_metric_failed_when_dadata_returns_503`        | Эмуляция падения DaData через `503 Service Unavailable`: запрос считается неуспешным, код ответа сохраняется в метрике. |
| `tests/test_dadata_client.py`   | `test_returns_error_metric_when_request_raises_timeout`   | Эмуляция падения DaData через сетевой `Timeout`: сервис возвращает `success=False`, `status_code=None` и текст ошибки.  |
| `tests/test_metrics_service.py` | `test_persists_metric_and_closes_session`                 | Метрика преобразуется в `ApiCheck`, добавляется в сессию, коммитится и соединение закрывается.                          |
| `tests/test_metrics_service.py` | `test_closes_session_even_when_commit_fails`              | Даже при ошибке БД во время `commit()` сессия корректно закрывается.                                                    |
| `tests/test_scheduler.py`       | `test_checks_all_endpoints_and_sleeps_between_iterations` | Scheduler проходит по всем endpoint'ам, передаёт метрики в `save_metric` и выдерживает интервал между итерациями.       |

## Результат последнего прогона тестов

Дата прогона: `2026-04-17`

Команда:

```bash
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

Итог:

```text
Ran 6 tests in 0.010s

OK
```

## Что было проанализировано

- Проект небольшой и разделён на понятные слои: HTTP-клиент, планировщик, сервис сохранения метрик и конфигурация.
- Основной операционный риск здесь связан с внешней зависимостью от DaData, поэтому в тесты отдельно добавлены сценарии деградации API.
- Unit-тесты изолируют сеть и БД, поэтому их можно запускать быстро и стабильно локально перед любыми изменениями.
