# Server

## Документация API

Доступ к API производится по адресу `https://bigcitylife.pythonanywhere.com/api/v1`

### Test
#### *Тестовый метод для проверки*
  > **[GET], [POST], [PUT], [DELETE]** `/test`
  
  **?..&..** Required args:
  ```
  Any or None
  ```
  **<-{}** Required data:
  ```
  Any or None
  ```
  **{}->** Answer:
  ```
  {
      'result': True,
      'received_args': <ARGS: dict>,
      'received_headers': <HEADERS: dict>,
      'received_json': <DATA: dict>
  }
   ```

### Users
#### Sign Up (Создать нового пользователя в NaviAddress)  
  > **[POST]** `/users/signup`
  
  **<-{}** Required data:
  ```
  {
      'email': str(50),
      'password': str,
      'first_name': str,
      'last_name': str
  }
  ```
  **{}->** Answer:
  ```
  {
      'email': str, 
      'first_name': str, 
      'gdpr_is_collect_analytic_data': bool, 
      'gdpr_is_receive_newsletter': bool, 
      'gdpr_is_restrict_user_data': bool, 
      'guest': bool, 
      'id': int, 
      'is_confirmed': bool, 
      'is_nps_sent': bool, 
      'last_name': str, 
      'nps': int, 
      'permissions': 
          {
              'event_addresses_limit': int, 
              'free_addresses_limit': int
          }, 
      'token': str
  }
  ```

#### Sign In  
  > **[POST]** `/users/signin`
  
  **<-{}** Required data:
  ```
  {
      'email': str(50),
      'password': str
  }
  ```
  **{}->** Answer:
  ```
  {
      'email': str, 
      'first_name': str, 
      'gdpr_is_collect_analytic_data': bool, 
      'gdpr_is_receive_newsletter': bool, 
      'gdpr_is_restrict_user_data': bool, 
      'guest': bool, 
      'id': int, 
      'is_confirmed': bool, 
      'is_nps_sent': bool, 
      'last_name': str, 
      'nps': int, 
      'permissions': 
          {
              'event_addresses_limit': int, 
              'free_addresses_limit': int
          }, 
      'token': str
  }
  ```

