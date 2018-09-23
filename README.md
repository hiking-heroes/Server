# Server

## Документация API

Доступ к API производится по адресу `https://........../api/v1`

### Users
* **[POST]** `/users/` - *Создать нового пользователя*  
  Словарь данных должен иметь ключи:
  * email,
  * password,
  * first_name,
  * last_name.
