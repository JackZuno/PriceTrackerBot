import datetime
import os
from dotenv import load_dotenv
from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import firebase_admin
from firebase_admin import credentials, firestore
from functions.users.manage_users import *
from functions.commands.commands import *

# Create a global list to store user chat IDs
user_chat_ids = {}

# List of available commands
available_commands = """
Here are the commands you can use:
1. /start - Start the bot
2. /auto - Enable automatic notifications
3. /list - List all items
4. /stop - Stop receiving notifications
5. /end - End the conversation
6. /help - Show available commands
"""

async def scheduled_message_pt1(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    try:
        # Send the scheduled message
        await context.bot.send_message(chat_id=chat_id, text="This is your first scheduled message!")
    except Exception as e:
        print(f"Error sending message to {chat_id}: {e}")

async def scheduled_message_pt2(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    try:
        # Send the scheduled message
        await context.bot.send_message(chat_id=chat_id, text="This is your second scheduled message!")
    except Exception as e:
        print(f"Error sending message to {chat_id}: {e}")


async def start_auto_messaging(update, context):
    chat_id = update.message.chat_id

    # Check if the user has already started the bot
    if (chat_id in user_chat_ids and user_chat_ids[chat_id]["started"] == False) or chat_id not in user_chat_ids:
        await update.message.reply_text("You need to use the /start command to interact with the bot.")
        return

    user_chat_ids[chat_id]["enabled"] = True

    # Schedule daily messages
    context.job_queue.run_daily(
        scheduled_message_pt1, 
        time=datetime.time(hour=10, minute=0), 
        days=(0, 1, 2, 3, 4, 5, 6), 
        chat_id=chat_id,  
        name=str(chat_id) 
    )

    context.job_queue.run_daily(
        scheduled_message_pt1, 
        time=datetime.time(hour=22, minute=0), 
        days=(0, 1, 2, 3, 4, 5, 6), 
        chat_id=chat_id,
        name=str(chat_id)  
    )

    # Notify the user that auto messaging has been enabled
    await context.bot.send_message(
        chat_id=chat_id, 
        text="Price changing notifications enabled ✔️",
        reply_markup=get_persistent_keyboard()
    )

async def stop_notify(update, context):
    chat_id = update.message.chat_id

    # Check if the user has already started the bot
    if (chat_id in user_chat_ids and user_chat_ids[chat_id]["started"] == False) or chat_id not in user_chat_ids:
        await update.message.reply_text("You need to use the /start command to interact with the bot.")
        return

    # Get all jobs by chat_id and remove them
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs:
        job.schedule_removal()

    # Mark the user as disabled for automatic messages
    user_chat_ids[chat_id]["enabled"] = False

    await context.bot.send_message(
        chat_id=chat_id, 
        text='Price changing notifications disabled ❌', 
        reply_markup=get_persistent_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    chat_id = update.message.chat_id

    # Check if the user already insert start
    if chat_id in user_chat_ids and user_chat_ids[chat_id]["started"] == True:
        await update.message.reply_text(available_commands, reply_markup=get_persistent_keyboard(), parse_mode='Markdown')
    else:
        await update.message.reply_text(available_commands, reply_markup=get_persistent_keyboard_after_end(), parse_mode='Markdown')

def get_persistent_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['/start', '/auto', '/stop', '/end', '/help'],  # List of commands in the keyboard
        ],
        one_time_keyboard=False,  # Keep the keyboard visible after the first press
        resize_keyboard=True  # Resize the keyboard to fit the screen
    )

def get_persistent_keyboard_after_end():
    return ReplyKeyboardMarkup(
        [
            ['/start', '/help'],  
        ],
        one_time_keyboard=False, 
        resize_keyboard=True  
    )

if __name__ == "__main__":
    # Load environment variables from the .env file
    load_dotenv()

    # Replace 'YOUR_BOT_TOKEN' with the token you got from BotFather
    bot_token = os.getenv("BOT_TOKEN")

    cred = credentials.Certificate('private/jackbotprice-firebase-adminsdk-b225s-a1fd9fc4c8.json')
    firebase_admin.initialize_app(cred)

    # Initialize Firestore DB
    db = firestore.client()

    # Create the application
    app = ApplicationBuilder().token(bot_token).build()

    # Add the /start command handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("auto", start_auto_messaging))
    app.add_handler(CommandHandler("stop", stop_notify))
    app.add_handler(CommandHandler("end", end))
    app.add_handler(CommandHandler("help", help_command))

    # Create the scheduler
    scheduler = BackgroundScheduler()

    # Start the scheduler
    scheduler.start()

    # Run the bot
    print("The bot is running")
    app.run_polling()
