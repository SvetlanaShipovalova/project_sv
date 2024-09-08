#### _Данный репозиторий содержит в себе 2 проекта на различных фреймворках, написанных на языке python._

***
# 1. Cайт транспортных перевозок на Flask

Проект представляет собой веб-сайт для отслеживания транспортных средств в пределах городской среды, разработанный с использованием Flask. Перед использованием приложения пользователю необходимо авторизироваться. Сайт предоставляет различный функционал в зависимости от роли, присвоенной администратором:
- Пассажиры имеют возможность авторизироваться на сайте и входить в систему для получения информации о местоположении и маршруте автобусов. 
- Водители могут открывать и закрывать рабочие смены. Также они имеют доступ к просмотру информации о других автобусах на линии маршрута.
- Администраторы — контролируют перевозки и состояние автобусов, могут редактировать информацию о пользователях, водителях и автобусах через админ-панель.

### Функциональные возможности
- Авторизация пользователей: Позволяет пользователям регистрироваться и входить в систему.
- Шифрование данных и подтверждение регистрации: после регистрации на почту приходит письмо с индивидуальной ссылкой для входа и подтверждения регистрации.
- Роли: Реализована система ролей, различающая права обычных пользователей и администраторов.
- Админ-панель: Обеспечивает управление пользователями и перевозками; администраторы могут просматривать, добавлять, редактировать и удалять записи.

### Используемые технологии
- Python
- Flask. Flask-Login. Flask-Admin.
- MySQL
- Bootstrap
- alembic
- SQLAlchemy
- Werkzeug
- WTForms
- Authlib
***
# 2. Магазин по продаже мониторов на Django

Проект представляет собой интернет-магазин, специализирующийся на продаже мониторов. 
Сайт позволяет пользователям добавлять заказы, редактировать и удалять их, а также отслеживать состояние доставки.

### Функциональные возможности
- Добавление заказов: Пользователи могут легко оформлять заказы на покупку мониторов.
- Удаление заказов: Возможность удаления ранее созданных заказов.
- Редактирование заказов: Возможность смены даты получения заказа на более поздний срок, если осталось более 10 суток до приезда заказа.
- Отслеживание состояния доставки: Пользователи могут проверять статус своих заказов и получать актуальную информацию о доставке.

### Используемые технологии
- Python
- Django
- MySQL