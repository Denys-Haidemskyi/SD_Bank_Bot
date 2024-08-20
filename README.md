
# SD_Bank_Bot

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
