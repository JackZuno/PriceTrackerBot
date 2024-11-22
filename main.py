import datetime
import os
import time
from dotenv import load_dotenv
from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

# Create a global list to store user chat IDs
user_chat_ids = {}

# List of available commands
available_commands = """
Here are the commands you can use:
1. /start - Start the bot
2. /auto - Enable automatic notifications
3. /stop - Stop receiving notifications
4. /end - End the conversation
5. /help - Show available commands
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_username = update.effective_user.username
    chat_id = update.effective_chat.id

    # Check if the user has already started the bot
    if chat_id in user_chat_ids and user_chat_ids[chat_id]["started"] == True:
        await update.message.reply_text("You have already started. You can use other commands now.")
        return

    msg = [
        f"Hi {user_username},\n\n",
        f"Welcome to *JackBotPrice*.\n\n",
        f"Here, you'll be able to receive notifications about price changes for specific items listed on Amazon.\n\n",
        f"To enable notifications for the inserted items, use the command */auto*.\n",
        f"To stop notifications for the inserted items, use the command */stop*.\n",
        f"To end the conversation with the bot, use the command */end*.\n\n",
        f"Enjoy your stay!\n\n",
        f"*Byeee!*"
    ]

    # Join all parts into a single string
    msg = ''.join(msg)

    # Store the user's chat ID
    if update.effective_chat.id not in user_chat_ids:
        user_chat_ids[update.effective_chat.id] = {"started": True, "enabled": False}
    else:
        user_chat_ids[update.effective_chat.id]["started"] = True

    # Send a message
    await update.message.reply_text(msg, reply_markup=get_persistent_keyboard(), parse_mode='Markdown')

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    # Check if the user has already started the bot
    if (chat_id in user_chat_ids and user_chat_ids[chat_id]["started"] == False) or chat_id not in user_chat_ids:
        await update.message.reply_text("You need to use the /start command to interact with the bot.")
        return

    # Remove scheduled jobs
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs:
        job.schedule_removal()

    # Remove the user from the user_chat_ids
    if chat_id in user_chat_ids:
        user_chat_ids[update.effective_chat.id]["started"] = False
        # del user_chat_ids[chat_id]
    
    print(user_chat_ids)

    # Send a confirmation message to the user
    await context.bot.send_message(
        chat_id=chat_id, 
        text="Your interaction with the bot has been ended. You will no longer receive messages.",
        reply_markup=get_persistent_keyboard_after_end()
    )

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
