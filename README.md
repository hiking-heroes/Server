# Server

## Документация API

Доступ к API производится по адресу `https://bigcitylife.pythonanywhere.com/api/v1`

## Оглавление
* [Test](#test)
  * [Тестовый метод для проверки](#Тестовый-метод-для-проверки)
* [Users](#users)
  * [Sign Up](#sign-up-Создать-нового-пользователя-в-naviaddress)
  * [Sign In](#sign-in)
* [Events](#events)
  * [Получить список ивентов для карты](#Получить-список-ивентов-для-карты)
  * [Получить иформацию по ивенту](#Получить-иформацию-по-ивенту)

### Test
#### Тестовый метод для проверки
* [Оглавление](#Оглавление)
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
* [Оглавление](#Оглавление)
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
    'guest': bool, 
    'id': int, 
    'email': str, 
    'first_name': str, 
    'last_name': str, 
    'token': str,
    'gdpr_is_collect_analytic_data': bool, 
    'gdpr_is_receive_newsletter': bool, 
    'gdpr_is_restrict_user_data': bool, 
    'is_confirmed': bool, 
    'is_nps_sent': bool, 
    'nps': int, 
    'permissions': 
      {
        'event_addresses_limit': int, 
        'free_addresses_limit': int
      }, 
    'events': []            - список будущих ивентов (пустой)
  }
  ```

#### Sign In  
* [Оглавление](#Оглавление)
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
    'guest': bool, 
    'id': int, 
    'email': str, 
    'first_name': str, 
    'last_name': str, 
    'token': str,
    'gdpr_is_collect_analytic_data': bool, 
    'gdpr_is_receive_newsletter': bool, 
    'gdpr_is_restrict_user_data': bool, 
    'is_confirmed': bool, 
    'is_nps_sent': bool, 
    'nps': int, 
    'permissions': 
      {
        'event_addresses_limit': int, 
        'free_addresses_limit': int
      }, 
    'events': [             - список будущих ивентов
      {
        'id': int,
        'container': str,
        'naviaddress': str,
        'owner_id': int,
        'latitude': float,
        'longitude': float,
        'type': str
      },
      ...
    ]
  }
  ```

### Events
#### Получить список ивентов для карты
* [Оглавление](#Оглавление)
  > **[GET]** `/events`
  
  **?..&..** Required args:
  ```
  ? lt_lat=float            - широта левой нижней точки
  & lt_lng=float            - долгота левой нижней точки
  & rb_lat=float            - широта правой верхней точки
  & rb_lng=float            - долгота правой верхней точки
  ```
  **?..&..** Optional args:
  ```
  & type=str                - тип ивента
  ```
  **{}->** Answer:
  ```
  {
    'events': [
      {
        'id': int,
        'container': str,
        'naviaddress': str,
        'owner_id': int,
        'latitude': float,
        'longitude': float,
        'type': str
      },
      ...
    ]
  }
  ```

#### Получить иформацию по ивенту
* [Оглавление](#Оглавление)
  > **[GET]** `/event/{id}`
  
  **{}->** Answer:
  ```
  {
    'id': int,
    'container': str,
    'naviaddress': str,
    'owner_id': int,
    'latitude': float,
    'longitude': float,
    'type': str,
    'navi' : {
      'name': str,
      'description': str,
      'booking': {
        'website': str,
        'caption': str,
        'telephone': str
      },
      'naviaddress': str,
      'container': str,
      'point': {
        'lat': int,
        'lng': int
      },
      'contacts': [
        {
          'type': str,
          'value': str
        },
        ...
      ],
      'event_start': datetime,
      'event_end': datetime,
      'address_description': {
        'floor': str,
        'building': str,
        'apartment': str,
        'intercom': str,
        'isoffice': bool
      },
      'last_mile': {
        'text': str,
        'type': str,
        'steps': [
          {
            'text': str,
            'image': str,
            'image_uuid': str
          },
          ...
        ]
      },
      'postal_address': str,
      'cover': [
        {
          'image_uuid': str,
          'image': str
        },
        ...
      ],
      'sharable_cover': [
        {
          'image_uuid': str,
          'image': str
        },
        ...
      ],
      'working_hours': [
        {
          'open_time': str,
          'close_time': str,
          'break_start_time': str,
          'break_end_time': str,
          'days': [
            str,
            ...
          ]
        },
        ...
      ],
      'map_visibility': bool,
      'category': {
        'id': int,
        'dbid': str,
        'name': str,
        'additional_name': str
      },
      'default_lang': str,
      'lang': str
    }
  }
  ```
