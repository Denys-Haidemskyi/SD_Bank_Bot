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

router = Router()

class TaskStatus(StatesGroup):
    name = State()
    desc = State()
    price = State()
    usr_id = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    create_time = dt.datetime.now()

    # Проверка наличия пользователя в базе данных
    sql_check_user = "SELECT * FROM users WHERE user_id = %s"
    mycursor.execute(sql_check_user, (user_id,))
    user = mycursor.fetchone()

    if user is None:
        # Если пользователь не найден, создаем новую запись
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
    tasks_keyboard = await create_tasks_keyboard()
    await message.answer('Вот список доступных заданий:', reply_markup=tasks_keyboard)

@router.callback_query(lambda c: c.data and c.data.startswith('task_'))
async def handle_task_selection(callback_query: CallbackQuery):
    # Извлекаем ID задачи из callback_data
    task_id = callback_query.data.split('_')[1]
    
    # Выполняем запрос к базе данных
    sql = 'SELECT task_name, description, reward FROM tasks WHERE task_id = %s'
    mycursor.execute(sql, (task_id,))  # Передаем task_id как кортеж с одним элементом
    task_name, description, reward = mycursor.fetchone()  # Извлекаем результат

    # Отправляем ответное сообщение
    await callback_query.message.answer(
        f'Задача номер: {task_id}\n📜<b>{task_name}</b>\n\n📋<i>{description}</i>\n\n{reward}💲', parse_mode='HTML'
    )

    # Подтверждаем обработку callback запроса
    await callback_query.answer()


class MakeTask():

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

        if balance_result is not None:
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
            await callback.message.answer('', reply_markup=kb.main)
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

    if balance_result is None:
        balance_clear = 0.0
    else:
        balance_clear = float(balance_result[0])

    await message.answer(f'Имя: {first_name}\nНомер счёта: {user_id}\nБаланс: {balance_clear} BKS')
