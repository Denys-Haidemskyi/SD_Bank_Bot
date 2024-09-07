from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bas.base import mycursor, mydb, mysql
import app.keyboards as kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from app.keyboards import create_tasks_keyboard, in_progress, WorkTasks, WhatAreDoing, Approve, howwedoit
import datetime as dt

router = Router()

class TaskStatus(StatesGroup):
    name = State()
    desc = State()
    price = State()
    usr_id = State()
    new_name = State()
    task_id_temp = State()
    new_desc = State()
    new_price = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    create_time = dt.datetime.now()

    sql_check_user = "SELECT * FROM users WHERE user_id = %s"
    mycursor.execute(sql_check_user, (user_id,))
    user = mycursor.fetchone()

    if user is None:
        sql_create_account = """
        INSERT INTO users (user_id, telegram_id, username, balance, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        val = (user_id, user_id, username, 0, create_time)
        mycursor.execute(sql_create_account, val)
        mydb.commit()

    await message.answer(f'Привет {first_name}, это бот S&D Bank, твой номер счёта {user_id}', reply_markup=kb.main)

@router.message(F.text == 'Задания📋')
async def tasks(message: Message):
    id = message.from_user.id
    tasks_keyboard = await create_tasks_keyboard(id)
    await message.answer('Вот список доступных заданий:', reply_markup=tasks_keyboard)

@router.callback_query(lambda c: c.data and c.data.startswith('task_'))
async def handle_task_selection(callback_query: CallbackQuery):
    task_id = callback_query.data.split('_')[1]
    
    sql = 'SELECT task_name, description, reward FROM tasks WHERE task_id = %s'
    mycursor.execute(sql, (task_id,))
    result = mycursor.fetchone()
    if result:
        task_name, description, reward = result
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.message.answer(
            f'Задача номер: {task_id}\n\n📜 <b>{task_name}</b>\n\n📋 <i>{description}</i>\n\n{reward}💲', parse_mode='HTML', reply_markup=kb.create_accept_task_keyboard(task_id)
        )
    else:
        await callback_query.message.answer("Ошибка: Задача не найдена.", reply_markup=kb.main)
    
    await callback_query.answer()

@router.callback_query(lambda c: c.data and c.data.startswith('accept_'))
async def accept_task(callback_query: CallbackQuery):
    task = callback_query.data.split('accept_')[1]

    sql_update = 'UPDATE tasks SET status = "in_progress" WHERE task_id = %s'
    '''sql_select = 'SELECT task_id FROM tasks WHERE task_id = %s'
    sql_get_task_id = mycursor.fetchone()''' 
    sql_add = 'INSERT INTO taskassignments (task_id, executor_id, status) VALUES (%s, %s, %s)'
    sql_add_task = (task, callback_query.from_user.id, "in_progress")
    mycursor.execute(sql_add, sql_add_task)
    mycursor.execute(sql_update, (task,))
    mydb.commit()
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer(f'Вы приняли задание номер {task}, можете приступать к выполнению!', reply_markup=kb.main)

@router.callback_query(lambda c: c.data and c.data.startswith('decline_'))
async def decline_T(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer(f'Возвращаем вас в меню!', reply_markup=kb.main)

@router.message(F.text == 'Создать задание📇')
async def makeTask(message: Message, state: FSMContext):
    await state.set_state(TaskStatus.name)
    await message.answer('Введите название задачи и отправьте')

@router.message(TaskStatus.name)
async def nameTask(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(TaskStatus.desc)
    await message.answer('Введите описание задания')

@router.message(TaskStatus.desc)
async def descTask(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await state.set_state(TaskStatus.price)
    await message.answer('Введите цену за выполнение')
    await state.update_data(usr_id=message.from_user.id)

@router.message(TaskStatus.price)
async def priceTask(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    x = data.get('name')
    y = data.get('desc')
    z = data.get('price')
    task_usr = data.get('usr_id')

    sql_get_balance = 'SELECT balance FROM users WHERE telegram_id = %s'
    mycursor.execute(sql_get_balance, (task_usr,))
    balance_result = mycursor.fetchone()

    if balance_result:
        balance = balance_result[0]
        if balance < int(z) or int(z) < 0:
            await message.answer(f'У вас нет денег на оплату задания, ваш баланс {balance}', reply_markup=kb.main)
        else:
            await message.answer(f'📜<b>{x}</b>\n\n📋<i>{y}</i>\n\n💲{z}\n\nПубликуем?', parse_mode='HTML', reply_markup=kb.publicu)
    else:
        await message.answer("Ошибка: не удалось получить баланс. Попробуйте позже.")

@router.callback_query(F.data == 'yes')
async def publicationTask(callback: CallbackQuery, state: FSMContext):
    create_time = dt.datetime.now()
    data = await state.get_data()
    task_name = data.get('name')
    task_desc = data.get('desc')
    task_price = data.get('price')
    task_usr = data.get('usr_id')

    try:
        sql_update_balance = 'UPDATE users SET balance = balance - %s WHERE telegram_id = %s'
        sql_insert_task = '''
        INSERT INTO tasks (creator_id, task_name, description, reward, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        sql_data = (task_usr, task_name, task_desc, task_price, 'open', create_time)
        sql_data_update = (task_price, task_usr)

        mycursor.execute(sql_update_balance, sql_data_update)
        mycursor.execute(sql_insert_task, sql_data)
        mydb.commit()

        await callback.message.answer('Задание опубликовано успешно!')
    except Exception as e:
        await callback.message.answer(f'Ошибка при публикации задания: {e}')
    finally:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer('Возвращаем вас в меню!', reply_markup=kb.main)
        await state.clear()

@router.callback_query(F.data == 'no')
async def dontPublicationTask(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('Публикация отменена, возвращаем вас в меню', reply_markup=kb.main)

@router.message(F.text == 'Профиль🤖')
async def profile(message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    balance_query = 'SELECT balance FROM users WHERE user_id = %s'
    mycursor.execute(balance_query, (user_id,))
    balance_result = mycursor.fetchone()

    if balance_result:
        balance_clear = float(balance_result[0])
    else:
        balance_clear = 0.0

    await message.answer(f'Имя: {first_name}\nНомер счёта: {user_id}\nБаланс: {balance_clear} BKS', reply_markup=kb.profile)

@router.message(F.text == 'Мои задания📇')
async def get_task(message: Message):
    usr = message.from_user.id
    get_task = await in_progress(usr)
    await message.answer('Вот список опубликованных заданий: ', reply_markup=get_task)

@router.callback_query(lambda c: c.data and c.data.startswith('tasks_'))
async def get_my_task(callback_query: CallbackQuery):
    task_id = callback_query.data.split('tasks_')[1]

    try:
        sql = 'SELECT task_name, description, reward, status, created_at FROM tasks WHERE task_id = %s'
        mycursor.execute(sql, (task_id,))
        data = mycursor.fetchone()

        if data:
            task_name, description, reward, status, created_at = data
        else:
            task_name = description = reward = status = created_at = "Неизвестно"
    finally:
        print('As good')

    # Отправка ответа
    reply_markup = kb.how(task_id)  # Убедитесь, что how возвращает InlineKeyboardMarkup
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer(
        f'Задача номер: {task_id}\n\n📜 <b>{task_name}</b>\n\n📋 <i>{description}</i>\n\n{reward}💲\n\nСтатус: {status}\nСоздано: {created_at}',
        parse_mode='HTML',
        reply_markup=reply_markup
    )

@router.callback_query(lambda c: c.data and c.data.startswith('delete_'))
async def delete_task(callback_query: CallbackQuery):
    delete_id = callback_query.data.split('delete_')[1]
    
    # Проверка соединения и создание нового курсора, если это необходимо
    if not mydb.is_connected():
        mydb.reconnect()
    mycursor = mydb.cursor()  # Создание нового курсора
    
    sql_del = 'DELETE FROM tasks WHERE task_id = %s'
    
    try:
        mycursor.execute(sql_del, (delete_id,))
        mydb.commit()
        await callback_query.message.bot.send_message(
            chat_id=callback_query.message.chat.id,
            text=f'Задача номер "{delete_id}" была удалена!'
        )
        await callback_query.message.delete()
    except mysql.connector.Error as err:
        await callback_query.message.bot.send_message(
            chat_id=callback_query.message.chat.id,
            text=f'Ошибка при удалении задачи: {err}'
        )
    finally:
        
        await callback_query.message.answer(f'Возвращаем вас в меню!', reply_markup=kb.main)

@router.callback_query(lambda c: c.data and c.data.startswith('change_'))
async def changeTask(callback_query: CallbackQuery):
    change_id = callback_query.data.split('change_')[1]
    reply_markup = kb.what_change(change_id)
    await callback_query.message.edit_reply_markup(reply_markup=reply_markup)

@router.callback_query(lambda c: c.data and c.data.startswith('taskName_'))
async def changeNameTask(callback_query: CallbackQuery, state: FSMContext):
    task_id_change = callback_query.data.split('taskName_')[1]
    await state.set_state(TaskStatus.new_name)
    await state.update_data(task_id_temp=task_id_change)
    await callback_query.message.answer(f'Введите новое название: ')

@router.message(TaskStatus.new_name)
async def NewTask(message: Message, state: FSMContext):
    await state.update_data(new_name=message.text)
    data = await state.get_data()
    new_id = data.get('new_name')
    task_id_temp = data.get('task_id_temp')

    if not mydb.is_connected():
        mydb.reconnect()
    mycursor = mydb.cursor()  # Создание нового курсора
    

    sql_new_name = 'UPDATE tasks SET task_name = %s WHERE task_id = %s'
    mycursor.execute(sql_new_name, (new_id, task_id_temp,))
    mydb.commit()
    await message.answer(f'Вы обновли название на {new_id}', reply_markup=kb.main)
    await state.clear()

@router.callback_query(lambda c: c.data and c.data.startswith('taskDescription_'))
async def changeNameTask(callback_query: CallbackQuery, state: FSMContext):
    task_id_change = callback_query.data.split('taskDescription_')[1]
    await state.set_state(TaskStatus.new_desc)
    await state.update_data(task_id_temp=task_id_change)
    await callback_query.message.answer(f'Введите новое описание: ')

@router.message(TaskStatus.new_desc)
async def NewTask(message: Message, state: FSMContext):
    await state.update_data(new_desc=message.text)
    data = await state.get_data()
    new_desc = data.get('new_desc')
    task_id_temp = data.get('task_id_temp')

    if not mydb.is_connected():
        mydb.reconnect()
    mycursor = mydb.cursor()  # Создание нового курсора
    

    sql_new_name = 'UPDATE tasks SET description = %s WHERE task_id = %s'
    mycursor.execute(sql_new_name, (new_desc, task_id_temp,))
    mydb.commit()
    await message.answer(f'Вы обновли описание на {new_desc}', reply_markup=kb.main)

@router.callback_query(lambda c: c.data and c.data.startswith('taskPrice_'))
async def changeNameTask(callback_query: CallbackQuery, state: FSMContext):
    task_id_change = callback_query.data.split('taskPrice_')[1]
    await state.set_state(TaskStatus.new_price)
    await state.update_data(task_id_temp=task_id_change)
    await callback_query.message.answer(f'Введите новую цену: ')

@router.message(TaskStatus.new_price)
async def NewTask(message: Message, state: FSMContext):
    await state.update_data(new_price=message.text)
    data = await state.get_data()
    new_price = data.get('new_price')
    task_id_temp = data.get('task_id_temp')

    if not mydb.is_connected():
        mydb.reconnect()
    mycursor = mydb.cursor()  # Создание нового курсора
    

    sql_new_name = 'UPDATE tasks SET reward = %s WHERE task_id = %s'
    mycursor.execute(sql_new_name, (new_price, task_id_temp,))
    mydb.commit()
    await message.answer(f'Вы обновли цену на {new_price}', reply_markup=kb.main)

@router.message(F.text == 'В работе📋')
async def inWork(message: Message):
    usr = message.from_user.id
    get_list = await WorkTasks(usr)
    await message.answer('Вот список задач в выполнении: ', reply_markup=get_list)

@router.callback_query(lambda c: c.data and c.data.startswith('WorkTaskId_'))
async def MyTask(callback: CallbackQuery):
    task_id = callback.data.split('WorkTaskId_')[1]
    sql_get = 'SELECT task_name, description, reward, status FROM tasks WHERE task_id = %s'
    mycursor.execute(sql_get, (task_id,))
    getted = mycursor.fetchall()
    howdo = WhatAreDoing(task_id)
    await callback.message.edit_reply_markup(reply_markup=None)
    for task_name, task_description, reward, status in getted:
        await callback.message.answer(f'📜<b>{task_name}</b>\n\n📋<i>{task_description}</i>\n\n💲{reward}\n\nStatus: {status}\n\nЧто делаем?', parse_mode='HTML', reply_markup=howdo)

@router.callback_query(lambda c: c.data and c.data.startswith('Delete_'))
async def DeleteTask(callback: CallbackQuery):
    delete_id = callback.data.split('Delete_')[1]
    sql_delete = 'DELETE FROM taskassignments WHERE task_id = %s'
    sql_update = 'UPDATE tasks SET status = %s WHERE task_id = %s'
    mycursor.execute(sql_delete, (delete_id,))
    mydb.commit()
    open = 'open'
    mycursor.execute(sql_update, (open, delete_id,))
    mydb.commit()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(f'Вы отказались от выполнения задания!', reply_markup=kb.main)

@router.callback_query(lambda c: c.data and c.data.startswith('Done_'))
async def Completed(callback: CallbackQuery):
    complete_id = callback.data.split('Done_')[1]
    
    # Обновление статуса задачи как завершенной
    sql_update = 'UPDATE taskassignments SET status = "completed" WHERE task_id = %s'
    mycursor.execute(sql_update, (complete_id,))
    mydb.commit()

    # Получение creator_id задачи, чтобы отправить сообщение создателю задачи
    sql_get = 'SELECT creator_id FROM tasks WHERE task_id = %s'
    mycursor.execute(sql_get, (complete_id,))
    getted = mycursor.fetchone()

    if getted:
        creator_id = getted[0]
        # Отправка сообщения создателю задачи
        await callback.message.bot.send_message(chat_id=creator_id, text="Привет, твоя задача была выполнена!, подтверди выполнение!")
    
    # Сообщение для исполнителя задачи
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Отмечено выполненым!", reply_markup=kb.main)

@router.callback_query(lambda c: c.data and c.data.startswith('back_'))
async def Back(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer(f'Назад', reply_markup=kb.main)

@router.message(F.text == 'Назад')
async def Back(message: Message):
    await message.answer(f'Возвращаем назад', reply_markup=kb.main)

@router.message(F.text == 'Ожидают подтверждения')
async def WaitToApprove(message: Message):
    user = message.from_user.id
    wait = await Approve(user)
    await message.answer(f'Список заданий ожидающих подтверждения: ', reply_markup=wait)

@router.callback_query(lambda c: c.data and c.data.startswith('taskap_'))
async def howwedo(callback: CallbackQuery):
    clean_task = callback.data.split('taskap_')[1]
    sql_get = 'SELECT task_name, description, reward FROM tasks WHERE task_id = %s'
    mycursor.execute(sql_get, (clean_task,))
    getted = mycursor.fetchall()
    call_func = await howwedoit(clean_task)
    await callback.message.edit_reply_markup(reply_markup=None)
    for task_name, desc, reward in getted:
        await callback.message.answer(f'📜<b>{task_name}</b>\n\n📋<i>{desc}</i>\n\n💲{reward}\n\nЧто делаем?', parse_mode='HTML', reply_markup=call_func)

@router.callback_query(lambda c: c.data and c.data.startswith('approve_'))
async def apTask(callback: CallbackQuery):
    user_id = callback.from_user.id
    clean_id = callback.data.split('approve_')[1]
    
    # Update the task status to "approved"
    sql_update = 'UPDATE taskassignments SET status = "approved" WHERE task_id = %s'
    mycursor.execute(sql_update, (clean_id,))
    mydb.commit()

    sql_update2 = 'SELECT executor_id FROM taskassignments WHERE task_id = %s'
    mycursor.execute(sql_update2, (clean_id,))
    gett = mycursor.fetchone()
    ex_id =gett[0]
    
    # Get the reward associated with the task
    sql_get_reward = 'SELECT reward FROM tasks WHERE task_id = %s'
    mycursor.execute(sql_get_reward, (clean_id,))
    getted_reward = mycursor.fetchone()
    
    if getted_reward:
        reward_amount = getted_reward[0]
        
        # Update the user's balance
        sql_update_user_balance = 'UPDATE users SET balance = balance + %s WHERE user_id = %s'
        mycursor.execute(sql_update_user_balance, (reward_amount, ex_id))
        mydb.commit()
        
        # Add a transaction record
        add_transaction = 'INSERT INTO transactions (user_id, task_id, amount, transaction_type) VALUES (%s, %s, %s, "reward")'
        mycursor.execute(add_transaction, (ex_id, clean_id, reward_amount))
        mydb.commit()
        
        # Optionally, delete the task if required
        sql_delete_task = 'UPDATE tasks SET status = "completed" WHERE task_id = %s'
        mycursor.execute(sql_delete_task, (clean_id,))
        mydb.commit()
        
        # Acknowledge the callback
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("Выполнение подтверждено!, награда выплачена.", reply_markup=kb.main)
    else:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("Task approval failed, reward not found.", reply_markup=kb.main)

@router.callback_query(lambda c: c.data and c.data.startswith('reject_'))
async def Reject(callback: CallbackQuery):
    clean_id = callback.data.split('reject_')[1]
    sql_get = 'SELECT executor_id FROM taskassignments WHERE task_id = %s'
    mycursor.execute(sql_get, (clean_id,))
    getted_id = mycursor.fetchone()
    sql_change = 'UPDATE taskassignments SET status = "rejected" WHERE task_id = %s'
    mycursor.execute(sql_change, (clean_id,))
    mydb.commit()
    if getted_id:
        ex = getted_id[0]
        await callback.message.bot.send_message(chat_id=ex, text='Задание было отклонено!, взгляни в заданиях')
