# Описание проекта

## Волга IT - Задание полуфинального этапа

В данном задании необходимо разработать сервис по аренде автомобилей
под названием “Simbir.GO”. Сервис предлагает аренду не только автомобилей, но и
мотоциклов, а также самокатов. Можно выбрать срок аренды транспортного
средства, например 1 минуту или 1 день.

В решении должна использована база данных Postgres. Авторизация пользователя 
осуществляется с помощью JWT (Json Web Token). Для проверки приложения 
сконфигурирован Swagger и с возможностью авторизации по JWT.

Swagger (http://127.0.0.1:5000/)

![Документация swagger](description/swagger.png)

### Account Controller API

![Документация Account Controller API](description/account_controller_api.png)

### Admin Account Controller API

![Документация Admin Account Controller API](description/admin_account_controller_api.png)

### Payment Controller API

![Документация Payment Controller API](description/payment_controller_api.png)

### Transport Controller API

![Документация Transport Controller API](description/transport_controller_api.png)

### Admin Transport Controller API

![Документация Admin Transport Controller API](description/admin_transport_controller_api.png)

### Rent Controller API

![Документация Rent Controller API](description/rent_controller_api.png)

### Admin Rent Controller API

![Документация Admin Rent Controller API](description/admin_rent_controller_api.png)

# Структура проекта

```
├───app
│   ├───apis
│   │   ├───accounts
│   │   ├───payments
│   │   ├───rents
│   │   └───transports
│   ├───configs
│   ├───core
│   │   ├───accounts
│   │   │   └───utils
│   │   ├───payments
│   │   ├───rents
│   │   └───transports
│   └───extensions
│       ├───database
│       │   ├───models
│       │   └───schemas
│       └───jwt
├───description 
└───tests  
```

Описание:
- В apis находится описание API в Swagger;
- В configs находятся конфиги для тестирования / отладки;
- В core находится бизнес-логика приложения;
- В extensions находятся сторонние библиотеки для Flask (ORM, JWT, ... );
- В test находятся unit-тесты для проверки корректной работы контроллеров.

# Запуск проекта 
```
docker compose up --build -d
```

Документация Swagger: http://127.0.0.1:5000



# Тестирование
Были протестированы следующие контроллеры:

- Account Controller
- Admin Account Controller
- Payment Controller
