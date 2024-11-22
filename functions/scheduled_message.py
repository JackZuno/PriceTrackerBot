from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from ..main import user_chat_ids

async def scheduled_message_pt1(context: ContextTypes.DEFAULT_TYPE) -> None:
    # Loop through all stored chat IDs and send the message
    for chat_id in user_chat_ids:
        try:
            # Send the scheduled message
            await context.bot.send_message(chat_id=chat_id, text="This is your first scheduled message!")
        except Exception as e:
            print(f"Error sending message to {chat_id}: {e}")

async def scheduled_message_pt2(context: ContextTypes.DEFAULT_TYPE) -> None:
    # Loop through all stored chat IDs and send the message
    for chat_id in user_chat_ids:
        try:
            # Send the scheduled message
            await context.bot.send_message(chat_id=chat_id, text="This is your second scheduled message!")
        except Exception as e:
            print(f"Error sending message to {chat_id}: {e}")