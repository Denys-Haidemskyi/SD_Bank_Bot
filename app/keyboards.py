from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from bas.base import mycursor, mydb
from aiogram.filters import CommandStart, Command
from aiogram import Router, types, Dispatcher
from bas.base import mycursor, mydb


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Профиль🤖')],
        [KeyboardButton(text='Задания📋'), KeyboardButton(text='Создать задание📇')],
        [KeyboardButton(text='Банк🏛️')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню...'
)

publicu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Да✅', callback_data='yes')],
        [InlineKeyboardButton(text='Нет❌', callback_data='no')],
    ]
)

async def handle_button(callback_query: types.CallbackQuery):
    # Скрытие инлайн-клавиатуры
    await callback_query.message.edit_reply_markup(reply_markup=None)
    # Ответ пользователю
    await callback_query.message.answer("Кнопка была нажата и скрыта.")

async def create_tasks_keyboard():
    # Выполнение SQL-запроса
    sql_get_task = 'SELECT task_id, task_name FROM tasks'
    mycursor.execute(sql_get_task)
    tasks_data = mycursor.fetchall()  # Вызов метода fetchall()

    # Создание клавиатуры для задач
    tasks_keyboard = InlineKeyboardMarkup(inline_keyboard=[])  # Убедитесь, что вы передаете пустой список

    # Создание строк кнопок
    buttons = []
    for task_id, task_name in tasks_data:
        button = InlineKeyboardButton(text=f'{task_name}', callback_data=f'task_{task_id}')
        buttons.append(button)
    
    # Разделение кнопок на строки (например, по 2 кнопки в строке)
    row_size = 2
    rows = [buttons[i:i + row_size] for i in range(0, len(buttons), row_size)]

    # Добавление строк в клавиатуру
    tasks_keyboard.inline_keyboard = rows

    return tasks_keyboard

