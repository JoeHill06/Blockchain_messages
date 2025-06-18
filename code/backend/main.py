from datetime import datetime
from flask import *
from flask_socketio import SocketIO, emit
import json
import random



# Simulated Users
users = [
    {"user_id": 1, "username": "Joe", "email": "joe@example.com", "password": "Joe", "profile_url": "https://i.pravatar.cc/300?img=12"},
    {"user_id": 2, "username": "Matt", "email": "matt@example.com", "password": "Matt", "profile_url": f"https://i.pravatar.cc/300?img={random.randint(1,15)}"},
    {"user_id": 3, "username": "Mum", "email": "mum@example.com", "password": "mum", "profile_url": f"https://i.pravatar.cc/300?img={random.randint(1,15)}"},
    {"user_id": 4, "username": "Alex", "email": "alex@example.com", "password": "Alex", "profile_url": f"https://i.pravatar.cc/300?img={random.randint(1,15)}"},
    {"user_id": 5, "username": "Sara", "email": "sara@example.com", "password": "Sara", "profile_url": f"https://i.pravatar.cc/300?img={random.randint(1,15)}"},
]

# Simulated Conversations
conversations = [
    {
        "conversation_id": 1,
        "participant_ids": [1, 2],
        "last_message_id": 1,
        "last_updated": datetime.now()
    },
    {
        "conversation_id": 2,
        "participant_ids": [1, 3],
        "last_message_id": 2,
        "last_updated": datetime.now()
    },
    {
        "conversation_id": 3,
        "participant_ids": [1, 4],
        "last_message_id": 4,
        "last_updated": datetime.now()
    },
    {
        "conversation_id": 4,
        "participant_ids": [2, 5],
        "last_message_id": 6,
        "last_updated": datetime.now()
    }
]

# Simulated Messages
messages = [
    {
        "message_id": 1,
        "conversation_id": 1,
        "sender_id": 1,
        "text": "Hey Matt!",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 2,
        "conversation_id": 1,
        "sender_id": 2,
        "text": "Hey joe!",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 3,
        "conversation_id": 1,
        "sender_id": 1,
        "text": "How are you!",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 4,
        "conversation_id": 3,
        "sender_id": 1,
        "text": "Hey Alex!",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 5,
        "conversation_id": 3,
        "sender_id": 4,
        "text": "Hi Joe, good to hear from you.",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 6,
        "conversation_id": 4,
        "sender_id": 2,
        "text": "Hi Sara!",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 7,
        "conversation_id": 4,
        "sender_id": 5,
        "text": "Hey Matt, how's your day?",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 8,
        "conversation_id": 2,
        "sender_id": 1,
        "text": "Hi Mum!",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 9,
        "conversation_id": 2,
        "sender_id": 3,
        "text": "Hello Joe, how was your day?",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 10,
        "conversation_id": 2,
        "sender_id": 1,
        "text": "It was good, thanks! How about yours?",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 11,
        "conversation_id": 1,
        "sender_id": 2,
        "text": "I'm doing great, what about you?",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 12,
        "conversation_id": 1,
        "sender_id": 1,
        "text": "Just chilling, working on my app.",
        "timestamp": datetime.now(),
        "status": "sent"
    }
]

app = Flask(__name__)
app.secret_key = "my_secret_key"
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/login", methods=["POST"])
def response():
    try:
        if request.method == "POST":
            data = request.get_json()
            username = data.get("username", '')
            password = data.get("password", '')

            for user in users:
                if user["username"] == username:
                    if user["password"] == password:
                        session["user"] = user
                        return jsonify({"login": "success"})

            return jsonify({"login": "failure", "message": "Invalid credentials"}), 401
    except Exception as e:
        print(e)
        return jsonify({"error": "Something went wrong"}), 500

@app.route("/getUserConversations", methods=["POST"])
def getUserConversations():
    try:
        if request.method == "POST":
            user = session["user"]
            chats = []

            for conversation in conversations:
                participants = conversation["participant_ids"]
                if user["user_id"] in participants:
                    other_user_id = next(pid for pid in participants if pid != user["user_id"])
                    other_user = next((u for u in users if u["user_id"] == other_user_id), {})
                    partner_username = other_user.get("username", "Unknown")
                    partner_profile_url = next(user["profile_url"] for user in users if user["user_id"] == other_user_id)

                    # Find the last message text
                    last_message_id = conversation["last_message_id"]
                    last_message = next((m for m in messages if m["message_id"] == last_message_id), {})
                    last_message_text = last_message.get("text", "")

                    # Debug print for conversation_id
                    print(f"Adding conversation with ID: {conversation['conversation_id']}")

                    chats.append({
                        "conversation_id": int(conversation["conversation_id"]),
                        "partner_user_id": other_user_id,
                        "user_id": user["user_id"],
                        "partner_username": partner_username,
                        "last_message": last_message_text,
                        "last_updated": conversation["last_updated"].isoformat(),
                        "partner_profile_url": partner_profile_url
                    })

            return jsonify({"conversations": chats})
    except Exception as e:
        print(e)
        return jsonify({"error": "Something went wrong"}), 500

@socketio.on('send_message')
def handle_send_message(data):
    # Extract and save new message
    new_message = {
        "message_id": len(messages) + 1,
        "conversation_id": int(data["conversation_id"]),
        "sender_id": session["user"]["user_id"],
        "text": data["text"],
        "timestamp": datetime.now(),
        "status": "sent"
    }
    messages.append(new_message)

    # Broadcast to all clients in this conversation
    emit('new_message', new_message, broadcast=True)


# Socket handler to fetch messages for a conversation
@socketio.on('get_messages')
def handle_get_messages(data):
    try:
        conversation_id = data.get("conversation_id")
        if conversation_id is None:
            emit("chat_messages", {"error": "Missing conversation_id"})
            return

        convo_messages = []
        for m in messages:
            if m["conversation_id"] == conversation_id:
                sender = next((u for u in users if u["user_id"] == m["sender_id"]), {})
                convo_messages.append({
                    "message_id": m["message_id"],
                    "conversation_id": int(m["conversation_id"]),
                    "sender_id": m["sender_id"],
                    "sender_username": sender.get("username", "Unknown"),
                    "text": m["text"],
                    "timestamp": m["timestamp"].isoformat(),
                    "status": m["status"]
                })
        emit("chat_messages", {"messages": convo_messages})
    except Exception as e:
        print(e)
        emit("chat_messages", {"error": "Failed to retrieve messages"})

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5003)
