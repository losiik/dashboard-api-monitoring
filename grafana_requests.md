1. Время ответа API (Latency)

```
SELECT
  checked_at AS time,
  response_time_ms,
  endpoint_type
FROM api_checks
WHERE $__timeFilter(checked_at)
ORDER BY checked_at
```

2. Доступность API (Availability)

```
SELECT
  checked_at AS time,
  endpoint_type,
  CASE
    WHEN success THEN 1
    ELSE 0
  END AS availability
FROM api_checks
WHERE $__timeFilter(checked_at)
ORDER BY checked_at
```

3. Количество ошибок
```
SELECT
  endpoint_type,
  count(*) AS errors
FROM api_checks
WHERE success = false
AND $__timeFilter(checked_at)
GROUP BY endpoint_type
```

4. Распределение HTTP статусов
```
SELECT
  status_code,
  count(*) AS total
FROM api_checks
WHERE $__timeFilter(checked_at)
GROUP BY status_code
ORDER BY total DESC
```

5. Среднее время ответа
```
SELECT
  endpoint_type,
  avg(response_time_ms) AS avg_latency
FROM api_checks
WHERE $__timeFilter(checked_at)
GROUP BY endpoint_type
```