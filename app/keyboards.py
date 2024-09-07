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
        [InlineKeyboardButton(text='Назад', callback_data=f'back_')]        
    ]
)

profile = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='В работе📋'), KeyboardButton(text='Мои задания📇')],
        [KeyboardButton(text='Ожидают подтверждения')],
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню...'
)

def how(task_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Изменить🔧', callback_data=f'change_{task_id}')],
            [InlineKeyboardButton(text='Удалить🗑️', callback_data=f'delete_{task_id}')],
            [InlineKeyboardButton(text='Назад', callback_data=f'back_')]
        ]
    )
async def in_progress(usr):
    sql_get_task = 'SELECT task_id, task_name FROM tasks WHERE creator_id = %s AND status = "open"'

    mycursor.execute(sql_get_task, (usr,))
    tasks_data = mycursor.fetchall()

    tasks_keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    buttons = []
    for task_id, task_name in tasks_data:
        button = InlineKeyboardButton(text=f'{task_name}', callback_data=f'tasks_{task_id}')
        buttons.append(button)
    
    row_size = 2
    rows = [buttons[i:i + row_size] for i in range(0, len(buttons), row_size)]

    tasks_keyboard.inline_keyboard = rows

    return tasks_keyboard

def create_accept_task_keyboard(task_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Принять✅', callback_data=f'accept_{task_id}')],
            [InlineKeyboardButton(text='Отклонить❌', callback_data=f'decline_{task_id}')],
            [InlineKeyboardButton(text='Назад', callback_data=f'back_')]
        ]
    
)

async def handle_button(callback_query: types.CallbackQuery):
    # Скрытие инлайн-клавиатуры
    await callback_query.message.edit_reply_markup(reply_markup=None)

async def create_tasks_keyboard(id):
    # Выполнение SQL-запроса
    sql_get_task = 'SELECT task_id, task_name FROM tasks WHERE status = "open" AND creator_id != %s'

    mycursor.execute(sql_get_task, (id,))
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

async def WorkTasks(usr):
    # Получаем все задания для пользователя
    sql_get = 'SELECT task_id FROM taskassignments WHERE executor_id = %s AND status = "in_progress" OR status = "rejected"'
    mycursor.execute(sql_get, (usr,))
    task_ids = mycursor.fetchall()  # Получаем все task_id для пользователя

    if task_ids:
        # task_ids - это список кортежей, поэтому нужно распаковать его
        task_names = []
        tasks_data = []  # Список для хранения пар (task_id, task_name)
        sql_get_task = 'SELECT task_name FROM tasks WHERE task_id = %s'
        
        for task_id_tuple in task_ids:
            task_id = task_id_tuple[0]  # Извлекаем task_id из кортежа
            mycursor.execute(sql_get_task, (task_id,))
            task_name = mycursor.fetchone()  # Получаем имя задания
            if task_name:  # Проверяем, что задание существует
                task_name = task_name[0]  # Извлекаем имя задания из кортежа
                task_names.append(task_name)  # Добавляем имя задания в список
                tasks_data.append((task_id, task_name))  # Добавляем пару (task_id, task_name) в tasks_data

        # Создаем клавиатуру для задач
        tasks_keyboard = InlineKeyboardMarkup(inline_keyboard=[])

        buttons = []
        for task_id, task_name in tasks_data:
            button = InlineKeyboardButton(text=f'{task_name}', callback_data=f'WorkTaskId_{task_id}')
            buttons.append(button)
        
        # Определяем размер строки
        row_size = 2
        rows = [buttons[i:i + row_size] for i in range(0, len(buttons), row_size)]

        tasks_keyboard.inline_keyboard = rows

        return tasks_keyboard
    else:
        print('Ошибка, заданий нету!',)

def what_change(change_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Название', callback_data=f'taskName_{change_id}')],
            [InlineKeyboardButton(text='Описание', callback_data=f'taskDescription_{change_id}')],
            [InlineKeyboardButton(text='Цена', callback_data=f'taskPrice_{change_id}')],
            [InlineKeyboardButton(text='Назад', callback_data=f'back_')]
        ]
    )

def WhatAreDoing(task_id):
    whatkeyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Выполнено✅', callback_data=f'Done_{task_id}')],
        [InlineKeyboardButton(text='Удалить🗑️', callback_data=f'Delete_{task_id}')],
        [InlineKeyboardButton(text='назад', callback_data=f'back_')],
    ])
    return whatkeyboard

async def Approve(user):
    # Получаем все задания с "in_progress" статусом
    sql_get = 'SELECT task_id FROM tasks WHERE creator_id = %s AND status = "in_progress"'
    mycursor.execute(sql_get, (user,))
    getted = mycursor.fetchall()
    
    # Список для хранения пар (task_id, task_name)
    tasks_data = []

    for task in getted:
        task_id = task[0]  # Получаем task_id из кортежа
        
        # Проверяем, завершено ли задание
        sql_get_new = 'SELECT task_id FROM taskassignments WHERE task_id = %s AND status = "completed"'
        mycursor.execute(sql_get_new, (task_id,))
        get_new = mycursor.fetchone()
        
        if get_new:  # Если задание завершено
            # Получаем имя задания
            sql_get_task_name = 'SELECT task_name FROM tasks WHERE task_id = %s'
            mycursor.execute(sql_get_task_name, (task_id,))
            task_name = mycursor.fetchone()
            
            if task_name:
                task_name = task_name[0]  # Извлекаем имя задания из кортежа
                tasks_data.append((task_id, task_name))  # Добавляем пару (task_id, task_name) в список

    if tasks_data:
        # Создаем клавиатуру для задач
        tasks_keyboard = InlineKeyboardMarkup(inline_keyboard=[])

        buttons = []
        for task_id, task_name in tasks_data:
            button = InlineKeyboardButton(text=f'{task_name}', callback_data=f'taskap_{task_id}')
            buttons.append(button)
        
        # Определяем размер строки
        row_size = 2
        rows = [buttons[i:i + row_size] for i in range(0, len(buttons), row_size)]

        tasks_keyboard.inline_keyboard = rows

        return tasks_keyboard
    else:
        print('Нет завершенных заданий')
        return None

async def howwedoit(id):
    kbdo = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Подтвердить✅', callback_data=f'approve_{id}')],
        [InlineKeyboardButton(text='Отказать❌', callback_data=f'reject_{id}')],
        [InlineKeyboardButton(text='Назад', callback_data=f'back_')]        
    ]
)
    return kbdo