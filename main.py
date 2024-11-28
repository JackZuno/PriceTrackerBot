import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters, CallbackQueryHandler
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
import firebase_admin
from firebase_admin import credentials, firestore
from functions.commands.commands import start, start_auto_messaging, stop_notify, end, remove_item, list_item, help_command, handle_remove_item, add_new_item, ASK_URL
from functions.commands.insert_url import cancel, handle_url
from functions.users.manage_users import post_init


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
    app = ApplicationBuilder().token(bot_token).post_init(post_init).build()

    # Define the conversation handler for adding a new item
    add_item_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("addItem", add_new_item)],
        states={
            ASK_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    add_item_conv_handler_emote_buttons = ConversationHandler(
        entry_points=[MessageHandler(filters.Text('🆕 Add Item'), add_new_item)],
        states={
            ASK_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url)],
        },
        fallbacks=[MessageHandler(filters.Text('❌Cancel'), cancel)],
    )

    # Command Handler 
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Text('🚀Start'), start))

    app.add_handler(CommandHandler("auto", start_auto_messaging))
    app.add_handler(MessageHandler(filters.Text('🔔Enable Notification'), start_auto_messaging))

    app.add_handler(CommandHandler("stop", stop_notify))
    app.add_handler(MessageHandler(filters.Text('🔕Disable Notification'), stop_notify))

    app.add_handler(CommandHandler("end", end))
    app.add_handler(MessageHandler(filters.Text('🛑Stop Bot'), end))

    app.add_handler(CommandHandler("remove", remove_item))
    app.add_handler(MessageHandler(filters.Text('🗑️Remove Item'), remove_item))

    app.add_handler(CommandHandler("list", list_item))
    app.add_handler(MessageHandler(filters.Text('📋List Items'), list_item))

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.Text('❓Help'), help_command))

    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(MessageHandler(filters.Text('❌Cancel'), cancel))

    app.add_handler(add_item_conv_handler)
    app.add_handler(add_item_conv_handler_emote_buttons)

    app.add_handler(CallbackQueryHandler(handle_remove_item))

    # Create and start the scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Run the bot
    print("The bot is running")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

