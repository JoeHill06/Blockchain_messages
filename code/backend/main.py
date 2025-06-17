from datetime import datetime
from flask import *
import json



# Simulated Users
users = [
    {"user_id": 1, "username": "Joe", "email": "joe@example.com", "password": "Joe"},
    {"user_id": 2, "username": "Matt", "email": "matt@example.com", "password": "Matt"},
]

# Simulated Conversations
conversations = [
    {
        "conversation_id": 1,
        "participant_ids": [1, 2],
        "last_message_id": 1,
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
    }
]

app = Flask(__name__)
app.secret_key = "my_secret_key"

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

                    # Find the last message text
                    last_message_id = conversation["last_message_id"]
                    last_message = next((m for m in messages if m["message_id"] == last_message_id), {})
                    last_message_text = last_message.get("text", "")

                    chats.append({
                        "conversation_id": conversation["conversation_id"],
                        "partner_username": partner_username,
                        "last_message": last_message_text,
                        "last_updated": conversation["last_updated"].isoformat()
                    })

            return jsonify({"conversations": chats})
    except Exception as e:
        print(e)
        return jsonify({"error": "Something went wrong"}), 500




if __name__ == "__main__":
    app.run(debug=True, port=5003)