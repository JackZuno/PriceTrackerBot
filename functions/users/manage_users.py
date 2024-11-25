

# Function to create or update user data in Firebase Firestore
def save_or_update_user_data(db, chat_id, username, first_name, bot_on=True, notifications_on=False):
    user_ref = db.collection('users').document(str(chat_id))
    
    user_data = {
        "chat_id": str(chat_id),
        "username": username,
        "first_name": first_name,
        "bot_on": bot_on,
        "notifications_on": notifications_on
    }

    # Save or update user data
    user_ref.set(user_data, merge=True)

# Function to retrieve user data from Firebase
def get_user_data(db, chat_id):
    user_ref = db.collection('users').document(str(chat_id))
    doc = user_ref.get()
    
    if doc.exists:
        return doc.to_dict()
    else:
        return None
