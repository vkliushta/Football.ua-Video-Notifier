import config
import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
from video_parser import parse

# Set log level
logging.basicConfig(level = logging.INFO)

# bot inizialization
bot = Bot(token = config.API_TOKEN)
dp = Dispatcher(bot)

# Іnitialize the connection to the database
db = SQLighter('db.db')

# Subscribe activation command
@dp.message_handler(commands = ['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # If there is no user, than add new user
        db.add_subscriber(message.from_user.id, True)
    else:
        # If there is user, than update subscribe status
        db.update_subscription(message.from_user.id, True)

    await message.answer("Yoy successfully subscribed to the newsletter!\nWait and soon you will know about new videos")    

# Unsubscribe activation command
@dp.message_handler(commands = ['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # If there is no user, than add new user with no active status
        db.add_subscriber(message.from_user.id, False)
        await message.answer("You are not subscribed")
    else:
        # If there is user, than update subscribe status
        db.update_subscription(message.from_user.id, False)
        await message.answer("You have unsubscribed")

 
# Check new video and if there is one send new video
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        # Parsing
        video = parse()

        if db.last_video()[0] != video:

            # Get bot subscribers
            subscriptions = db.get_subscriptions()
            # Send message
            for s in subscriptions:
                if s[2]:
                    await bot.send_message(s[1], f'Hi! Here is a new video from football.ua. Enjoy\n\n{video}')

            db.update_video(video)

# Start long polling
if __name__ == '__main__':
    dp.loop.create_task(scheduled(5))
    executor.start_polling(dp, skip_updates = True)