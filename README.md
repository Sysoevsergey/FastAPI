run database
```bash
docker-compose --env-file .env up db
```

run migrations
```bash
docker-compose --env-file .env up migrate
```

run api
```bash
docker-compose --env-file .env up app
```

run tests
```bash
docker-compose --env-file .env up tests
```

# Домашнее задание к лекции «Создание REST API на FastApi» часть 1

Инструкцию по сдаче домашнего задания Вы найдете на главной странице репозитория.

# Задание 
Вам нужно написать на fastapi и докеризировать сервис объявлений купли/продажи.

У объявлений должны быть следующие поля:
 - заголовок
 - описание
 - цена
 - автор
 - дата создания

Должны быть реализованы следующе методы:
 - Создание: `POST /advertisement`
 - Обновление: `PATCH /advertisement/{advertisement_id}`
 - Удаление: `DELETE /advertisement/{advertisement_id}`
 - Получение по id: `GET  /advertisement/{advertisement_id}`
 - Поиск по полям: `GET /advertisement?{query_string}`

Авторизацию и аутентификацию реализовывать **не нужно**

# Задание 

Вам нужно доработать проект из предыдущего задания «Создание REST API на FastApi» часть 1:

1. Добавить роут `POST /login` . В теле запроса должен передаваться JSON с именем пользователя и паролем.  Роут возвращает токен. В дальнейшем токен будет использоваться для авторизации.  Срок действия токена - 48 часов. Если клиент предоставил неверный логин пароль сервис должен выдать ошибку 401. 

2. Добавить роуты для управления пользователями:
- `GET /user/{user_id?}`
- `POST /user` 
- `PATCH /user/{user_id} `
- `DELETE /user/{user_id}`

  Пользователи должны принадлежать одной из следующих групп: user, admin

3. Права неавторизованного пользователя (клиент может токен не передавать):
- Создание пользователя `POST /user`
- Получение пользователя по id `GET /user/{user_id}`
- Получение объявления по id  `GET /advertisement/{advertisement_id}`
- Поиск объявления по полям `GET /advertisement?{query_string}`

4. Права авторизованного пользователя с группой user:
- все права неавторизованного пользователя
- обновление своих данных `PATCH /user/{user_id}`
- удаление себя `DELETE /user/{user_id}`
- создание объявления  `POST /advertisement`
- обновление своего объявления `PATCH /advertisement/{advertisement_id}`
- удаление своего объявления `DELETE /advertisement/{advertisement_id}`

5. Права авторизованного пользователя с группой admin:
- любые действия с любыми сущностям

Если у пользователя недостаточно прав для выполнения операции, то возвращается ошибка 403