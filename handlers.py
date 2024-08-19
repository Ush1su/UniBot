from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from openai import OpenAI
import keyboards as kb

router = Router()
client = OpenAI(
    organization='org-qT3TXRA7xLWXCjgrgS9TjYam',
    api_key="sk-proj-MJvO3mBuuYoq66Q1xDobT3BlbkFJ6rUrAGitwI1LTkbTkgCN",
)


class Node(StatesGroup):
    user_spec = State()
    user_reg = State()
    user_scholar = State()
    user_messages = State()


async def start_que(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Node.user_spec)
    await message.answer(f'Complete the surveys below to get advice', reply_markup=await kb.reply_spec())


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        f'What\'s up {message.from_user.first_name}. I am bot that can help you to find university and scholarship for you.')
    await start_que(message, state)


@router.message(Node.user_spec and F.text.in_(kb.spec))
async def second_que(message: Message, state: FSMContext):
    await state.update_data(user_spec=message.text)
    await state.set_state(Node.user_reg)
    await message.answer(f'Choose region where you wanna study', reply_markup=await kb.reply_reg())


@router.message(Node.user_reg and F.text.in_(kb.regions))
async def reg_que(message: Message, state: FSMContext):
    await state.update_data(user_reg=message.text)
    await state.set_state(Node.user_scholar)
    await message.answer(f'Scholarship?', reply_markup=kb.get_scholarship)


@router.message(F.text == "Back to first choice")
async def back(message: Message, state: FSMContext):
    await start_que(message, state)


@router.message(F.text == "Advise more universities")
async def more(message: Message, state: FSMContext):
    cont = "Advise more universitites with the same parametres"
    data = await state.get_data()
    content = data['user_messages']
    content.append({"role": "user", "content": cont})
    wait_message = await message.answer('Wait a bit...')
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=content,
    )
    text = stream.choices[0].message.content
    content.append({"role": "system", "content": text})
    await state.update_data(user_messages=content)
    text = text.replace('*', '')
    text = text.replace('#', '')
    await wait_message.edit_text(text)
    await message.answer("Wanna more?", reply_markup=kb.after)


@router.message(Node.user_scholar and F.text.in_(kb.sch))
async def give_answer(message: Message, state: FSMContext):
    await state.update_data(user_scholar=message.text)
    data = await state.get_data()
    print(data)
    cont = f'I wanna study {data['user_spec']} undergraduate in {data['user_reg']} in english'
    add_part = ". Advice me universities. Write it as a list of Universitites and programs there. Give a link to university site main page. Also write some scholarshipd available for international studsent"
    if (data['user_scholar'] == 'Necessary'):
        cont += " with scholarship"
    cont += add_part
    print(cont)
    wait_message = await message.answer('Wait a bit...')
    content = [{"role": "user", "content": cont}]
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=content,
    )
    text = stream.choices[0].message.content
    content.append({"role": "system", "content": text})
    await state.update_data(user_messages=content)
    text = text.replace('*', '')
    text = text.replace('#', '')
    await wait_message.edit_text(text)
    await message.answer("Wanna more?", reply_markup=kb.after)
