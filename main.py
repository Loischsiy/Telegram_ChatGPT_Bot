import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

token = 'your_token_bot'

openai.api_key = 'your_api_key'

memory = {}

bot = Bot(token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def cmd_start_help(message: types.Message):
    if message.text == '/start':
        await message.answer("Привет! Я бот ChatGPT, у тебя какие-то вопросы? (Для очистки запросов напишите /clear)")
    elif message.text == '/help':
        await message.answer("Для очистки запросов напишите /clear")

@dp.message_handler(commands=['clear'])
async def cmd_clear(message: types.Message):
  user_id = message.from_user.id
  memory[user_id] = ""
  await message.answer("История запросов очищенна!!!")

@dp.message_handler()
async def send(message : types.Message):
    with open("log.txt", "a") as f:
      f.write(f"{message.from_user.id} : {message.text}\n")
    user_id = message.from_user.id
    if user_id not in memory:
        # Добавляем пользователя в словарь, если его там еще нет
        memory[user_id] = "" 
    # Обновляем историю запросов
    memory[user_id] = memory[user_id] + message.text + "\n"
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=memory[user_id],
      temperature=0.9,
      max_tokens=1000,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.6,
      stop=["You:"]
)

    await message.answer(response['choices'][0]['text'])

executor.start_polling(dp, skip_updates=True)
