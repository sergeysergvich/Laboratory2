import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token='7054508113:AAExLieCizMeW9cvmz2yRRa81Ens9nR9kco') # Создаем экземпляр класса Bot для взаимодействия с Telegram API, передаем токен
dp = Dispatcher(bot) # Создаем экземпляр класса Dispatcher для управления обработчиками сообщений

questions = [ # Заисываем вопросы викторины как список словарей
    {
        'question': 'Какое насекомое вызвало короткое замыкание в ранней версии вычислительной машины, тем самым породив термин «компьютерный баг»?',
        'options': ['Мотылек', 'Таракан', 'Муха', 'Японский хрущик'],
        'answer': '1',
        'image': 'https://wl-adme.cf.tsp.li/resize/728x/webp/baf/48c/bbf9945900a71afb49c85703f0.jpg.webp',
        'welcome_image': 'https://cdn.cadelta.ru/media/covers/4/id4664/cover.jpg'
    },
    {
        'question': 'Какой химический элемент составляет более половины массы тела человека?',
        'options': ['Углерод', 'Кальций', 'Кислород', 'Железо'],
        'answer': '3',
        'image': 'https://wl-adme.cf.tsp.li/resize/728x/webp/927/1f3/dcc4405de6bc398fff085f5c4d.jpg.webp'
    },
    {
        'question': 'Какой футболист принёс победу сборной Росии по футболу в матче против Испании на ЧМ-2018?',
        'options': ['Фёдор Смолов', 'Игорь Акинфеев', 'Марио Фернандес', 'Артём Дзюба'],
        'answer': '2',
        'image':'https://cdn.iz.ru/sites/default/files/styles/2048x1365/public/photo_item-2018-07/1530467133_2.JPG?itok=WS0E5gRR'
    },
    {
        'question': 'Какого цвета крайнее правое кольцо в олимпийской символике?',
        'options': ['Желтое', 'Зеленое', 'Синее', 'Красное'],
        'answer': '4',
        'image' :'https://wl-adme.cf.tsp.li/resize/728x/webp/47b/0ff/18099b517385b9f2fe84f344a4.jpg.webp'
    },
    {
        'question': 'Что означает гавайское слово «вики», которое дало название интернет-энциклопедии «Википедия»?',
        'options': ['Простой', 'Изученный', 'Быстрый', 'Умный'],
        'answer': '3',
        'image' :'https://wl-adme.cf.tsp.li/resize/728x/webp/bd7/606/1b754650059c4d5f845acca207.jpg.webp'
    }

]
@dp.message_handler(commands=['start']) # Обработчик сообщений для команды /start
async def start_game(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = { # Добавляем данные пользователя, такие как счет и номер вопроса
        'score': 0,
        'question_number': 0,
        'questions_asked': []
    }
    await ask_question(user_id) # Задаем пользователю первый вопрос

async def ask_question(user_id): # Функция для задавания вопроса пользователю
    user_question_data = user_data[user_id]
    question_number = user_question_data['question_number'] # Текущий номер вопроса
    if question_number >= len(questions): # Проверяем, не закончились ли вопросы
        await bot.send_message(user_id, f'Вы ответили на все вопросы! Ваш счет: {user_question_data["score"]}')
        await bot.send_photo(user_id, photo='https://i.ytimg.com/vi/a2wxKWKHLO4/maxresdefault.jpg')
        return # Сообщаем о завершении игры и показываем результат
    question = questions[question_number]
    options = '\n'.join([f'{i+1}. {option}' for i, option in enumerate(question['options'])]) # Отправляем вопрос и варианты ответов пользователю
    await bot.send_message(user_id, f'{question["question"]}\n\n{options}')
    user_question_data['question_number'] += 1

@dp.message_handler() # Обработчик для ответов на вопросы
async def answer_question(message: types.Message):
    user_id = message.from_user.id
    user_question_data = user_data[user_id]
    question_number = user_question_data['question_number'] - 1
    if question_number < 0 or question_number >= len(questions):
        return
    question = questions[question_number]
    answer = question['answer']
    if message.text == answer: # Проверяем правильность ответа пользователя
        user_question_data['score'] += 100 # Начисляем очки за правильный ответ и отправляем изображение
        await bot.send_message(user_id, 'Правильно! Вы заработали 100 очков.')
        question_image_url = question['image']
        await bot.send_photo(user_id, question_image_url)
    else:
        await bot.send_message(user_id, f'Неправильно. Правильный ответ: {answer}.') # Информируем о неправильном ответе
    await ask_question(user_id)


if __name__ == '__main__':
    user_data = {}
    executor.start_polling(dp, skip_updates=True)