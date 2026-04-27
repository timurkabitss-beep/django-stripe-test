# Django + Stripe Payment Gateway

## Описание
Простой сервер на Django с интеграцией Stripe для создания платежных форм.

## Функционал
- **Модель Item** (название, описание, цена)
- **Модель Order** (заказы с несколькими товарами)
  - OrderItem с фиксацией цены на момент покупки
  - Автоматический расчёт итоговой суммы
- **Stripe Checkout Session**
- **Django Admin** для управления товарами
- **API endpoints:**
  * GET /item/<id> - страница товара с кнопкой Buy
  * GET /buy/<id> - создание Stripe Session

## Запуск локально

### Требования
- Python 3.10+
- Docker (опционально)

### Установка
1. Клонируйте репозиторий
2. Создайте `.env` файл,
в нём должны быть ВАШИ данные:
```bash
SECRET_KEY=your-secret-key
DEBUG=True
STRIPE_SECRET_KEY=sk_test_<ваш_ключ...>
STRIPE_PUBLISHABLE_KEY=pk_test_<ваш_ключ...>
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Примените миграции
```bash
python manage.py migrate
```
5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```
6. Запустите сервер:
```bash
python manage.py runserver 
```

## Docker
```bash
docker-compose up --build
```

## Тестирование
* Зайдите в админку: http://localhost:8000/admin
* Создайте тестовый Item
* Откройте http://localhost:8000/item/1
* Нажмите Buy

