### Login

**POST**`/auth/login/`

* **Описание**: Аутентификация пользователя по логину и паролю.
* **Тело запроса**:

  ```
  {
  "username": "string",
  "password": "string"
  }
  ```

  * **Ответ**:
  ```
  {
  "token": "string"
  }
  ```
### Registration

**POST**`/auth/register/`

* **Описание**: Регистрация нового пользователя.
* **Тело запроса**:
  ```
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
* **Ответ**:
  ```
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "token": "string"
  }
  ```
### Logout

**POST**`/auth/logout/`

* **Описание**: Выход из системы.
* **Заголовки**: Необходимо передавать токен авторизации.
* **Ответ**:
  {
    "detail": "Successfully logged out."
  }

---

## Menu

### Get Menu Items

**GET**`/menu-items/` ?category=

* **Описание**: Получить список всех пунктов меню.
* **Ответ**:
  ```
  [
    {
      "id": 1,
      "name": "string",
      "description": "string",
      "category": "string",
      "price": "decimal"
    }
  ]
  ```

### Create Menu Item

**POST**`/menu-items/`

* **Описание**: Создать новый пункт меню (для администратора).
* **Тело запроса**:
  ```
  {
    "name": "string",
    "description": "string",
    "category": "string",
    "price": "decimal"
  }
  ```

* **Ответ**:
  ```
  {
    "id": 1,
    "name": "string",
    "description": "string",
    "category": "string",
    "price": "decimal"
  } 
  ```

### Get Menu Item

**GET**`/menu-items/{id}/`

* **Описание**: Получить информацию о конкретном пункте меню по его ID.
* **Ответ**:
  ```
  {
    "id": 1,
    "name": "string",
    "description": "string",
    "category": "string",
    "price": "decimal"
  }
  ```

### Update Menu Item

**PUT**`/menu-items/{id}/`

* **Описание**: Обновить информацию о пункте меню (для администратора).
* **Тело запроса**:
  ```
  {
    "name": "string",
    "description": "string",
    "price": "decimal"
  }
  ```

### Delete Menu Item

**DELETE**`/menu-items/{id}/`

* **Описание**: Удалить пункт меню по ID (для администратора).

---

## Orders

### Get Orders

**GET**`/orders/`

* **Описание**: Получить список всех заказов (для администратора).
* **Ответ**:
  ```
  [
    {
      "id": 1,
      "user_id": 1,
      "items": [1, 2, 3],
      "total_price": "decimal",
      "status": "string"
    }
  ]
  ```

### Create Order

**POST**`/orders/`

* **Описание**: Создать новый заказ.
* **Тело запроса**:
  ```
  {
    "items": [1, 2, 3]
  }
  ```

* **Ответ**:
  ```
  {
    "id": 1,
    "user_id": 1,
    "items": [1, 2, 3],
    "total_price": 1,
    "status": "pending"
  }
  ```

### Get Order

**GET**`/orders/{id}/`

* **Описание**: Получить информацию о конкретном заказе по его ID.
* **Ответ**:
  ```
  {
    "id": 1,
    "user_id": 1,
    "items": [1, 2, 3],
    "total_price": "decimal",
    "status": "string"
  }
  ```

### Update Order Status

**PATCH**`/orders/{id}/status/`

* **Описание**: Обновить статус заказа (для администратора).
* **Тело запроса**:
  ```
  {
    "status": "string"
  }
  ```

---

## Users

### Get Users

**GET**`/users/`

* **Описание**: Получить список всех пользователей (для администратора).
* **Ответ**:
  ```
  [
    {
      "id": 1,
      "username": "string",
      "email": "string",
      "role": "string"
    }
  ]
  ```

### Create User

**POST**`/users/`

* **Описание**: Создать нового пользователя.
* **Тело запроса**:
  ```
  {
    "username": "string",
    "password": "string",
    "email": "string"
  }
  ```

### Get User

**GET**`/users/{id}/`

* **Описание**: Получить информацию о конкретном пользователе по ID.
* **Ответ**:
  ```
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "role": "string"
  }
  ```

---

## Order Statuses

### Get Order Statuses

**GET**`/order-statuses/`

* **Описание**: Получить список возможных статусов заказа.
* **Ответ**:
  ```
  [
    {
      "status": "pending"
    },
    {
      "status": "completed"
    },
    {
      "status": "cancelled"
    }
  ]
  ```

---

## Add to Cart
### POST /cart/add/

* **Описание**: Добавляет элемент меню в корзину текущего пользователя.
* **Тело запроса**:
  ```
  {
    "menu_item_id": 1,
    "quantity": 2
  }
  ```
* **Ответ**:
  ```
  {
    "id": 1,
    "user": "username",
    "menu_item": {
      "id": 1,
      "name": "Tomato Soup",
      "price": "4.99"
    },
    "quantity": 2,
    "total_price": "9.98"
  }
  ```
## Clear Cart
### DELETE /cart/clear/

* **Описание**: Очищает корзину текущего пользователя.
* **Ответ**:
  ```
  {
    "message": "Cart has been cleared."
  }
  ```

## Checkout
### POST /checkout/

* **Описание**: Оформление заказа. Включает адрес доставки, время доставки (ближайшее или выбор диапазона).
* **Тело запроса**:
  ```
  {
    "delivery_address": "123 Main St, Apt 4B",
    "delivery_time": "nearest"  // либо "timeslot"
  }
  ```
* **Ответ**:
  ```
  {
    "order_id": 123,
    "message": "Order has been placed successfully.",
    "delivery_details": {
      "address": "123 Main St, Apt 4B",
      "delivery_time": "2024-10-20 18:00:00"
    },
    "total_price": "29.99"
  }
  ```

## Get Available Delivery Time Slots
### GET /delivery-timeslots/

* **Описание**: Возвращает доступные временные диапазоны для доставки.
* **Ответ**:
  ```
  [
    {
      "id": 1,
      "start_time": "2024-10-20 18:00:00",
      "end_time": "2024-10-20 19:00:00"
    },
    {
      "id": 2,
      "start_time": "2024-10-20 19:00:00",
      "end_time": "2024-10-20 20:00:00"
    }
  ]
  ```