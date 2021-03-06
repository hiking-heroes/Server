# Server
[![CodeFactor](https://www.codefactor.io/repository/github/hiking-heroes/server/badge)](https://www.codefactor.io/repository/github/hiking-heroes/server)
# Документация API
***
**NOTE**
* Доступ к API производится по адресу `https://bigcitylife.pythonanywhere.com/api/v1`  
* В методах, где требуется отправить JSON данные, в HEADERS должно быть указано `"content-type": "application/json"`
***
## Оглавление
* [Test](#test)
  * [Тестовый метод для проверки](#Тестовый-метод-для-проверки)
* [Users](#users)
  * [Sign Up](#sign-up-Создать-нового-пользователя-в-naviaddress)
  * [Sign In](#sign-in)
* [Events](#events)
  * [Получить список ивентов для карты](#Получить-список-ивентов-для-карты)
  * [Получить иформацию по ивенту](#Получить-иформацию-по-ивенту)
  * [Создать ивент](#Создать-ивент)
  * [Присоединиться к ивенту](#Присоединиться-к-ивенту)
  * [Покинуть ивент](#Покинуть-ивент)
  * [Список всех ивентов пользователя](#Список-всех-ивентов-пользователя)
* [Notifications](#notifications)
  * [Подписать устройство на уведомления](#Подписать-устройство-на-уведомления)
  * [Отписать устройство от уведомлений](#Отписать-устройство-от-уведомлений)
  * [Получить список подписанных на уведомления девайсов](#Получить-список-подписанных-на-уведомления-девайсов)

## Test
### Тестовый метод для проверки
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
  **{}->** Answer: *200*
  ```
  {
    'result': True,
    'received_args': <ARGS: dict>,
    'received_headers': <HEADERS: dict>,
    'received_json': <DATA: dict>
  }
   ```

## Users
### Sign Up (Создать нового пользователя в NaviAddress)  
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
  **{}->** Answer: *201*  
  [Full User](#full-user)

### Sign In  
* [Оглавление](#Оглавление)
  > **[POST]** `/users/signin`
  
  **<-{}** Required data:
  ```
  {
    'email': str(50),
    'password': str
  }
  ```
  **{}->** Answer: *200*  
  [Full User](#full-user)
  

## Events
### Получить список ивентов для карты
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
  & start=str               - datetime начала интервала
  & end=str                 - datetime конца
  & tags=str,...            - список тегов через ","
  ```
  **{}->** Answer: *200*
  ```
  {
    'events': [
      {
        'id': int,
        'name': str,
        'container': str,
        'naviaddress': str,
        'owner_id': int,
        'latitude': float,
        'longitude': float,
        'type': str,
        'seats' {
          'total': int or null,
          'free': int or null
        },
        'tags': [
          str,
          ...
        ]
      },
      ...
    ]
  }
  ```

### Получить иформацию по ивенту
* [Оглавление](#Оглавление)
  > **[GET]** `/events/{id}`
  
  **{}->** Answer: *200*  
  [Full Event](#full-event)

### Создать ивент
* [Оглавление](#Оглавление)
  > **[POST]** `/events`
  
  **^{}** Required header's data:
  ```
  {
    'Authorization': str    - token
  }
  ```
  **<-{}** Required data:
  ```
  {
    'lat': float,
    'lng': float,
    'name': str,
    'event_start': str,
    'event_end': str
  }
  ```
  **<-{}** Optional args:
  ```
  {
    'description': str,
    'web': str
    'type': str,
    'default_lang': str,
    'lang': str,
    'map_visibility': bool,
    'seats': str,
    'tags': [
      str,
      ...
    ]
  }
  ```
  **{}->** Answer: *201*  
  [Full Event](#full-event)
  
### Присоединиться к ивенту
* [Оглавление](#Оглавление)
  > **[PUT]** `/events/{id}/join`
  
  **^{}** Required header's data:
  ```
  {
    'Authorization': str    - token
  }
  ```
  **{}->** Answer: *200*  
  [Full Event](#full-event)

### Покинуть ивент
* [Оглавление](#Оглавление)
  > **[PUT]** `/events/{id}/exit`
  
  **^{}** Required header's data:
  ```
  {
    'Authorization': str    - token
  }
  ```
  **{}->** Answer: *200*  
  [Full Event](#full-event)
  
### Список всех ивентов пользователя
* [Оглавление](#Оглавление)
  > **[GET]** `/events/my`
  
  **^{}** Required header's data:
  ```
  {
    'Authorization': str    - token
  }
  ```
  **?..&..** Optional args:
  ```
  & type=str                - тип ивента
  & start=str               - datetime начала интервала
  & end=str                 - datetime конца
  & tags=str,...            - список тегов через ","
  ```
  **{}->** Answer: *200*  
  ```
  {
    'events': [
      {
        'id': int,
        'name': str,
        'container': str,
        'naviaddress': str,
        'owner_id': int,
        'latitude': float,
        'longitude': float,
        'type': str,
        'seats' {
          'total': int or null,
          'free': int or null
        },
        'tags': [
          str,
          ...
        ]
      },
      ...
    ]
  }
  ```

## Notifications
### Подписать устройство на уведомления
* [Оглавление](#Оглавление)
  > **[POST]** `/notifications/devices`
  
  **^{}** Required header's data:
  ```
  {
    'Authorization': str    - token
  }
  ```
  **<-{}** Required data:
  ```
  {
    "device_token": str
  }
  ```
  **{}->** Answer: *201*
  ```
  {
    'id': int,
    'token': str
  }
  ```

### Отписать устройство от уведомлений
* [Оглавление](#Оглавление)
  > **[DELETE]** `/notifications/devices/{id}`
  
  **^{}** Required header's data:
  ```
  {
    'Authorization': str    - token
  }
  ```
  **{}->** Answer: *200*
  ```
  [                         - list of subscribed devices
    {
      'id': int,
      'token': str
    },
    ...
  ]
  ```
  
### Получить список подписанных на уведомления девайсов 
* [Оглавление](#Оглавление)
  > **[GET]** `/notifications/devices`
  
  **^{}** Required header's data:
  ```
  {
    'Authorization': str    - token
  }
  ```
  **{}->** Answer: *200*
  ```
  [                         - list of subscribed devices
    {
      'id': int,
      'token': str
    },
    ...
  ]
  ```
  
## Модели
### Full User
* [Оглавление](#Оглавление)
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
  'events': [             - список ивентов
    {
      'id': int,
      'name': str,
      'container': str,
      'naviaddress': str,
      'owner_id': int,
      'latitude': float,
      'longitude': float,
      'type': str,
      'seats' {
        'total': int or null,
        'free': int or null
      },
      'tags': [
        str,
        ...
      ]
    },
    ...
  ]
}
```
### Full Event
* [Оглавление](#Оглавление)
```
{
  'id': int,
  'name': str,
  'container': str,
  'naviaddress': str,
  'owner_id': int,
  'latitude': float,
  'longitude': float,
  'type': str,
  'seats' {
    'total': int or null,
    'free': int or null
  },
  'tags': [
    str,
    ...
  ],
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
