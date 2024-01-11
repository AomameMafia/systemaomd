from phone import phone_al
YOUR_BOT_TOKEN = "6841906698:AAFutA0gnWCFPOQZO5cx02kpaVYwzx_pRzM"
import re
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import json
import os

# Функция, которая будет вызываться при получении сообщения с цифрами и эмодзи 🟢
def process_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id  # Получаем идентификатор пользователя
    chat_id = update.message.chat_id  # Получаем идентификатор чата
    if update.message.chat.type == 'private':  # Проверяем, является ли чат личным сообщением
        update.message.reply_text('Извините, этот бот работает только там где нужно. Пишите @AomameMafia.')
        return
    text = update.message.text
    match = re.search(r'(-?\d+)🟢\s+Пункт\s+(\d{1,2})\.\s+(.+)', text)
    if match:
        user_id = str(user_id)
        value = int(match.group(1))
        point_number = int(match.group(2))
        if not 1 <= point_number <= 18:  # Проверяем, что номер пункта находится в диапазоне от 1 до 18
            update.message.reply_text('Такого пункта нет! Номер пункта должен быть от 1 до 18.')
            return
        if not os.path.isfile(f'sums_{user_id}.json'):  # При необходимости инициализируем файл "sums_{user_id}.json" для данного пользователя
            with open(f'sums_{user_id}.json', 'w') as file:
                json.dump({}, file)
        with open(f'sums_{user_id}.json', 'r') as file:
            data = json.load(file)
        data[str(point_number)] = data.get(str(point_number), 0) + value
        with open(f'sums_{user_id}.json', 'w') as file:
            json.dump(data, file)
        point_values = [f"Пункт {k}: {v}" for k, v in data.items()]
        sum_values = sum(data.values())
        update.message.reply_text('\n'.join(point_values + [f'Сумма всех пунктов: {sum_values}']))  # Отправляем значения в чат вместе со суммой
    else:
        update.message.reply_text('Оформи как нужно! Правила оформления в самом первом закрепе')

# Главная функция
def main() -> None:
    updater = Updater(YOUR_BOT_TOKEN)  # Укажите токен вашего бота

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.all & (~Filters.command), process_message))
    updater.start_polling()
    updater.idle()

phone_al()
if __name__ == '__main__':
    main()
