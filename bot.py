from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery,
                           Message, BotCommand)
import texts
import time

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage: MemoryStorage = MemoryStorage()

# Создаем объекты бота и диспетчера
bot: Bot = Bot('')
dp: Dispatcher = Dispatcher(storage=storage)


class FSMFillForm(StatesGroup):
    fill_1 = State()
    fill_2 = State()
    fill_3 = State()
    fill_4 = State()
    fill_5 = State()
    fill_6 = State()


# Создаем объекты инлайн-кнопок
big_button_2 = InlineKeyboardButton(
    text='пройти тест',
    callback_data='big_button_2_pressed')

big_button_yes = InlineKeyboardButton(
    text='да',
    callback_data='yes_pressed')

big_button_no = InlineKeyboardButton(
    text='нет',
    callback_data='no_pressed')


# Создаем объект инлайн-клавиатуры
keyboard2 = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_2]])

keyboard3 = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_yes, big_button_no]])



# Этот хэндлер будет срабатывать на команду /start
@dp.message(CommandStart())
async def command_start(message: Message, state: State):
    time.sleep(3)
    await message.answer(text=texts.text1, parse_mode='HTML')
    time.sleep(12)
    await message.answer(text=texts.text2, parse_mode='HTML', reply_markup=keyboard2)
    await state.set_state(FSMFillForm.fill_1)


# 1 вопрос
@dp.callback_query(F.data == 'big_button_2_pressed', StateFilter(FSMFillForm.fill_1))
async def test_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=texts.text2, parse_mode='HTML')
    await bot.send_message(chat_id=callback.message.chat.id, text=texts.question1, reply_markup=keyboard3)

# обработка ответов
# верный ответ ответ на 1 вопрос
@dp.callback_query(F.data == 'yes_pressed', StateFilter(FSMFillForm.fill_1))
async def answer_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=texts.question1)
    await bot.send_message(chat_id=callback.message.chat.id, text=texts.question2, reply_markup=keyboard3)
    await state.set_state(FSMFillForm.fill_2)

# неверный ответ ответ на 1 вопрос
@dp.callback_query(F.data == 'no_pressed', StateFilter(FSMFillForm.fill_1))
async def answer_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await bot.send_message(chat_id=callback.message.chat.id, text=texts.question11, reply_markup=keyboard3)

# верный ответ ответ на 2 вопрос
@dp.callback_query(F.data == 'yes_pressed', StateFilter(FSMFillForm.fill_2))
async def answer_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=texts.question2)
    await bot.send_message(chat_id=callback.message.chat.id, text=texts.question3, reply_markup=keyboard3)
    await state.set_state(FSMFillForm.fill_3)

# неверный ответ ответ на 2 вопрос
@dp.callback_query(F.data == 'no_pressed', StateFilter(FSMFillForm.fill_2))
async def answer_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await bot.send_message(chat_id=callback.message.chat.id, text=texts.question21, reply_markup=keyboard3)

# верный ответ ответ на 3 вопрос
@dp.callback_query(F.data == 'no_pressed', StateFilter(FSMFillForm.fill_3))
async def answer_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=texts.question3)
    await bot.send_message(chat_id=callback.message.chat.id, text=texts.question4, reply_markup=keyboard3)
    await state.set_state(FSMFillForm.fill_4)

# неверный ответ ответ на 3 вопрос
@dp.callback_query(F.data == 'yes_pressed', StateFilter(FSMFillForm.fill_3))
async def answer_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await bot.send_message(chat_id=callback.message.chat.id, text=texts.question31, reply_markup=keyboard3)

# верный ответ ответ на 4 вопрос
@dp.callback_query(F.data == 'yes_pressed', StateFilter(FSMFillForm.fill_4))
async def answer_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=texts.question4)
    await bot.send_message(chat_id=callback.message.chat.id, text=texts.question5, reply_markup=keyboard3)
    await state.set_state(FSMFillForm.fill_5)

# неверный ответ ответ на 4 вопрос
@dp.callback_query(F.data == 'no_pressed', StateFilter(FSMFillForm.fill_4))
async def answer_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await bot.send_message(chat_id=callback.message.chat.id, text=texts.question41, reply_markup=keyboard3)

# верный ответ ответ на 5 вопрос
@dp.callback_query(F.data == 'no_pressed', StateFilter(FSMFillForm.fill_5))
async def answer_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=texts.question5)
    time.sleep(5)
    await bot.send_message(chat_id=callback.message.chat.id, text=texts.text3, parse_mode='HTML')
    await state.set_state(FSMFillForm.fill_6)

# неверный ответ ответ на 5 вопрос
@dp.callback_query(F.data == 'yes_pressed', StateFilter(FSMFillForm.fill_5))
async def answer_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await bot.send_message(chat_id=callback.message.chat.id, text=texts.question51, reply_markup=keyboard3)

# Запускаем пуллинг
if __name__ == '__main__':
    dp.startup()
    dp.run_polling(bot, skip_updates=False)
