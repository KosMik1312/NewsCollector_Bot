import asyncio
import logging
from telethon import TelegramClient, events

# Настройка логирования
logging.basicConfig(level=logging.INFO)  # Уровень логирования
logger = logging.getLogger(__name__)

# Используйте свои данные для подключения к API Telegram
api_id = '111111'
api_hash = 'd1b41......'

# Указываем каналы для сбора и отправки сообщений
from_channel_usernames = ['https://t.me/gtrkmariel',
                          'https://t.me/topyo_media',
                          'https://t.me/yoshka12_chp',
                          'https://t.me/rian_ru'
]  # Список каналов

to_channel_username = 'https://t.me/newscollectorr' # Целевой канал

client = TelegramClient('gbot', api_id, api_hash,
                        system_version='4.16.30-vxCUSTOM',
                        device_model='Infinix',
                        app_version='1.0.0'
) # Клиент

# Основная функция
async def main():
    logger.info("Запуск основной функции...")
    # Указываем ID каналов
    source_channel_entities = [await client.get_input_entity(username) for username in from_channel_usernames]

    # Получаем одно последнее сообщение из каждого исходного канала
    for source_channel_entity in source_channel_entities:
        last_message = await client.get_messages(source_channel_entity, limit=1)
        logger.info(f"Пересылаем сообщение из {source_channel_entity} в {to_channel_username}")
        await client.send_message(to_channel_username, last_message[0])

# Обработка нового сообщения
@client.on(events.NewMessage(chats=from_channel_usernames))
async def handle_new_message(event):
    message = event.message
    logger.info(f"Получено новое сообщение из {event.chat.title}: {message.text}")
    await client.send_message(to_channel_username, message)
    await asyncio.sleep(300)  # задержка на 5 минут

# Запускаем клиент и ждем, пока он не будет отключен
async def start_client():
    logger.info("Запуск клиента...")
    await client.start()
    await main()
# Запуск клиента
client.loop.run_until_complete(start_client())
client.run_until_disconnected()
