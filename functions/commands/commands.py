from telegram import Update
from telegram.ext import ContextTypes
from functions.users.manage_users import *
from firebase_admin import firestore
from functions.keyboard.keyboard import *

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    chat_id = update.effective_chat.id

    # Initialize Firestore DB
    db = firestore.client()

    # Check if the user has the bot already on
    user_data = get_user_data(db, chat_id)

    # Check if the user exists and the bot is already running
    # with .get('bot_on', True) it return something only if the field is true
    if user_data and user_data.get('bot_on') == True:
        await update.message.reply_text("You have already started the bot 🤖. You can use other commands now.")
        return

    # Save or update user data in Firebase
    save_or_update_user_data(db, chat_id, username, first_name)

    msg = [
        f"Hi {username},\n\n",
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

    # Send a message
    await update.message.reply_text(msg, reply_markup=get_persistent_keyboard(), parse_mode='Markdown')


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    # Initialize Firestore DB
    db = firestore.client()

    # Retrieve the user
    user_data = get_user_data(db, chat_id)

    if not user_data or (user_data and user_data.get('bot_on') == False):
        await update.message.reply_text("You need to use the /start command to interact with the bot.")
        return

    # Set the bot_on and notifications_on variables to false (notifications_on is set to False by default)
    user_data["bot_on"] = False
    save_or_update_user_data(db, chat_id, user_data['username'], user_data['first_name'], user_data['bot_on'], user_data['notifications_on'])

    # Remove scheduled jobs
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs:
        job.schedule_removal()
    
    # Send a confirmation message to the user
    await context.bot.send_message(
        chat_id=chat_id, 
        text="Your interaction with the bot has been ended. You will no longer receive messages.",
        reply_markup=get_persistent_keyboard_after_end()
    )