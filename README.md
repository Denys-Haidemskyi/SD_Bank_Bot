# SD_Bank_Bot

## English (EN-USA)

### Description

**SD_Bank_Bot** is a Telegram bot developed for internal use within a family. The bot allows users to create accounts, complete tasks, and earn rewards in the form of internal currency called Buks (BKS). Users can transfer Buks between accounts or request a withdrawal to real currency (EUR) based on the internal exchange rate.

### Main Features

- **Account Creation**: Each user can create their own account.
- **Task Creation and Completion**: Users can create tasks and set rewards in BKS. Other users can accept these tasks and earn the reward.
- **Fund Transfer**: Ability to transfer Buks between accounts.
- **Withdrawal Request**: Users can request to withdraw Buks to real currency.

### Technical Details

- **Programming Language**: Python
- **Libraries Used**:
  - `aiogram`: for interacting with the Telegram API and managing the bot.
  - `mysql.connector`: for working with a MySQL database.
  - `datetime`: for handling date and time.

Example of imports:

```python
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bas.base import mycursor, mydb
import app.keyboards as kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from app.keyboards import create_tasks_keyboard
import datetime as dt
import mysql.connector
```

### Installation and Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/YourUsername/SD_Bank_Bot.git
   cd SD_Bank_Bot
   ```

2. **Database Setup**:

   - Start your MySQL database.
   - Enter the correct database details in the `base.py` file.

3. **Install Dependencies**:

   - Ensure you have Python 3.6 or later installed.
   - Install the required dependencies using pip:
     ```bash
     pip install aiogram mysql-connector-python
     ```

4. **Run the Bot**:
   - Run the bot script:
     ```bash
     python bot.py
     ```

### Usage Instructions

1. **Start**: Enter the `/start` command in the chat with the bot.
2. **Navigation**: Use the buttons provided by the bot to create accounts, tasks, and perform other actions.

### Support and Contact

If you have any questions or suggestions, feel free to contact the developer:

- Telegram: [Denys Haidemskyi](https://t.me/Denys_Haidemskyi)
- Instagram: [denys.haidemskyi](https://www.instagram.com/denys.haidemskyi/)

---

## Русский (RU-Russian)

### Описание

**SD_Bank_Bot** — это Telegram-бот, разработанный для внутреннего использования в семье. Бот позволяет создавать аккаунты, выполнять задания и получать за них вознаграждение во внутренней валюте, именуемой буксами (BKS). Пользователи могут переводить буксы между аккаунтами или запросить их вывод в реальной валюте (евро), согласно внутреннему курсу.

### Установка и запуск

1. **Клонирование репозитория**:

   ```bash
   git clone https://github.com/YourUsername/SD_Bank_Bot.git
   cd SD_Bank_Bot
   ```

2. **Настройка базы данных**:

   - Запустите MySQL базу данных.
   - Внесите корректные данные базы в файл `base.py`.

3. **Установка зависимостей**:

   - Убедитесь, что у вас установлен Python 3.6 или выше.
   - Установите зависимости с помощью pip:
     ```bash
     pip install aiogram mysql-connector-python
     ```

4. **Запуск бота**:
   - Запустите файл с ботом:
     ```bash
     python bot.py
     ```

### Инструкции по использованию

1. **Запуск**: Введите команду `/start` в чате с ботом.
2. **Навигация**: Используйте кнопки, предоставляемые ботом, для создания аккаунта, заданий и выполнения других действий.

### Поддержка и связь

Если у вас возникли вопросы или предложения, свяжитесь с разработчиком:

- Telegram: [Denys Haidemskyi](https://t.me/Denys_Haidemskyi)
- Instagram: [denys.haidemskyi](https://www.instagram.com/denys.haidemskyi/)

---

## Українська (UA-Ukrainian)

### Опис

**SD_Bank_Bot** — це Telegram-бот, розроблений для внутрішнього використання в сім'ї. Бот дозволяє створювати облікові записи, виконувати завдання та отримувати за них винагороду у внутрішній валюті, що називається букси (BKS). Користувачі можуть переводити букси між обліковими записами або запитувати їх виведення у реальну валюту (євро) згідно з внутрішнім курсом.

### Встановлення та налаштування

1. **Клонування репозиторію**:

   ```bash
   git clone https://github.com/YourUsername/SD_Bank_Bot.git
   cd SD_Bank_Bot
   ```

2. **Налаштування бази даних**:

   - Запустіть базу даних MySQL.
   - Внесіть правильні дані бази у файл `base.py`.

3. **Встановлення залежностей**:

   - Переконайтеся, що у вас встановлено Python 3.6 або пізнішу версію.
   - Встановіть необхідні залежності за допомогою pip:
     ```bash
     pip install aiogram mysql-connector-python
     ```

4. **Запуск бота**:
   - Запустіть файл із ботом:
     ```bash
     python bot.py
     ```

### Інструкції з використання

1. **Запуск**: Введіть команду `/start` у чаті з ботом.
2. **Навігація**: Використовуйте кнопки, надані ботом, для створення облікових записів, завдань та виконання інших дій.

### Підтримка та зв'язок

Якщо у вас виникли питання або пропозиції, звертайтеся до розробника:

- Telegram: [Denys Haidemskyi](https://t.me/Denys_Haidemskyi)
- Instagram: [denys.haidemskyi](https://www.instagram.com/denys.haidemskyi/)

---

## Español (ES-Español)

### Descripción

**SD_Bank_Bot** es un bot de Telegram desarrollado para uso interno dentro de una familia. El bot permite a los usuarios crear cuentas, completar tareas y ganar recompensas en forma de moneda interna llamada Buks (BKS). Los usuarios pueden transferir Buks entre cuentas o solicitar un retiro a moneda real (EUR) según la tasa de cambio interna.

### Instalación y Configuración

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/YourUsername/SD_Bank_Bot.git
   cd SD_Bank_Bot
   ```

2. **Configuración de la base de datos**:

   - Inicia tu base de datos MySQL.
   - Ingresa los datos correctos de la base de datos en el archivo `base.py`.

3. **Instalar Dependencias**:

   - Asegúrate de tener instalado Python 3.6 o posterior.
   - Instala las dependencias necesarias usando pip:
     ```bash
     pip install aiogram mysql-connector-python
     ```

4. **Ejecutar el Bot**:
   - Ejecuta el script del bot:
     ```bash
     python bot.py
     ```

### Instrucciones de Uso

1. **Inicio**: Ingresa el comando `/start` en el chat con el bot.
2. **Navegación**: Utiliza los botones proporcionados por el bot para crear cuentas, tareas y realizar otras acciones.

### Soporte y Contacto

Si tienes alguna pregunta o sugerencia, no dudes en contactar al desarrollador:

- Telegram: [Denys Haidemskyi](https://t.me/Denys_Haidemskyi)
- Instagram: [denys.haidemskyi](https://www.instagram.com/denys.haidemskyi/)
