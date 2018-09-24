# Server

## Документация API

Доступ к API производится по адресу `https://bigcitylife.pythonanywhere.com/api/v1`

### Test
* *Тестовый метод для проверки*
  > **[GET], [POST], [PUT], [DELETE]** `/test`
  
  Может принимать любый аргументы и данные.
  В ответ вернет словарь 
  ```
  {
      'result': True,
      'received_args': <ARGS: dict>,
      'received_headers': <HEADERS: dict>,
      'received_json': <DATA: dict>
   }
   ```

### Users
* *Создать нового пользователя*  
  > **[POST]** `/users`
  
  Словарь данных должен иметь ключи:
  * email,
  * password,
  * first_name,
  * last_name.
