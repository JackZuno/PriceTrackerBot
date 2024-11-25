from telegram import ReplyKeyboardMarkup

# List of available commands
available_commands = """
Here are the commands you can use:
1. /start - Start the bot
2. /auto - Enable automatic notifications
3. /stop - Stop receiving notifications
4. /end - End the conversation
5. /help - Show available commands
"""

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