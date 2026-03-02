## Примеры запросов

Для начала нужно зарегистрировать пользователя
: Отправить POST-запрос на эндпоинт `'auth/users/'` и передать в нём поля:

```json
  {
      "email": "testuser@example.com",
      "password": "СложныйПароль123",
      "username": "testuser"
  }
```

Получение токена

: Отправить POST-запрос на эндпоинт `'auth/jwt/create/'` и передать в нём поля:

```json
  {
      "email": "testuser@example.com",
      "password": "СложныйПароль123",
      "username": "testuser"
  }
```

В ответе от API в поле`"token"`вы получите токен. Сохраните его.

Создание повода

: Отправить POST-запрос на эндпоинт `occasion/` и передать в него обязательное поле `name`, в заголовке указать тот самый скопированный ранее токен:`Authorization`:`Bearer <токен>`.

1. Пример запроса:

   ```json
      {
          "name": "Праздник"
      }
   ```

2. Пример ответа:

   ```json
      {
          "id": 2,
          "name": "Праздник"
      }
   ```

Создание сбора

: Отправить POST-запрос на эндпоинт `collects/` и передать в него обязательные поля `name`(id повода) и `description`,'final_sum', 'completion_datetime' в заголовке так же обязательно указать токен как в предыдущем примере.

1. Пример запроса:

   ```json
      {
        "name": "Сбор денег",

        "author": "user@example.com",

        "description": "Собираем на праздник",

        "occasion": "1",

        "final_sum": 15000,

        "completion_datetime": "2025-10-15"
      }
   ```

2. Пример ответа:

   ```json
      {
        "id": 15,
        "name": "Сбор денег",
        "description": "Собираем на праздник",
        "current_sum": 1000,
        "final_sum": 15000,
        "collect_image": null,
        "completion_datetime": "2025-10-15",
        "created_datetime": "2025-08-11T17:16:30.884402Z",
        "author": 7,
        "occasion": 1,
        "contributors_count": 1
     }
   ```
Создание платежа
: Отправить POST-запрос на эндпоинт `payment/`:

1. Пример запроса:

   ```json
      {
        "sum": 1000,
        "collect": "1"
      }
   ```
2. Пример ответа:

   ```json
      {
        "sum": 1000,
        "payment_datetime": "2025-08-26T12:57:03.721680Z",
        "contributor": 804
      }
   ```
