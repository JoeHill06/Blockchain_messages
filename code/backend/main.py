from datetime import datetime
from flask import *
from flask_socketio import SocketIO, emit
import json
import random
import hashlib
import datetime as dt
import hashlib
import json

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash, message_data=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(dt.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'messages': message_data or []
        }
        self.chain.append(block)
        return block

    def print_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1
        return True

# Simulated Users
users = [
    {"user_id": 1, "username": "User1", "email": "user1@example.com", "password": "Joe", "profile_url": "https://i.pravatar.cc/300?img=12"},
    {"user_id": 2, "username": "User2", "email": "user2@example.com", "password": "Matt", "profile_url": f"https://i.pravatar.cc/300?img={random.randint(1,15)}"},
    {"user_id": 3, "username": "User3", "email": "user3@example.com", "password": "mum", "profile_url": f"https://i.pravatar.cc/300?img={random.randint(1,15)}"},
    {"user_id": 4, "username": "User4", "email": "user4@example.com", "password": "Alex", "profile_url": f"https://i.pravatar.cc/300?img={random.randint(1,15)}"},
    {"user_id": 5, "username": "User5", "email": "user5@example.com", "password": "Sara", "profile_url": f"https://i.pravatar.cc/300?img={random.randint(1,15)}"},
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
        "text": "Sample message 1",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 2,
        "conversation_id": 1,
        "sender_id": 2,
        "text": "Sample message 2",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 3,
        "conversation_id": 1,
        "sender_id": 1,
        "text": "Sample message 3",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 4,
        "conversation_id": 3,
        "sender_id": 1,
        "text": "Sample message 4",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 5,
        "conversation_id": 3,
        "sender_id": 4,
        "text": "Sample message 5",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 6,
        "conversation_id": 4,
        "sender_id": 2,
        "text": "Sample message 6",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 7,
        "conversation_id": 4,
        "sender_id": 5,
        "text": "Sample message 7",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 8,
        "conversation_id": 2,
        "sender_id": 1,
        "text": "Sample message 8",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 9,
        "conversation_id": 2,
        "sender_id": 3,
        "text": "Sample message 9",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 10,
        "conversation_id": 2,
        "sender_id": 1,
        "text": "Sample message 10",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 11,
        "conversation_id": 1,
        "sender_id": 2,
        "text": "Sample message 11",
        "timestamp": datetime.now(),
        "status": "sent"
    },
    {
        "message_id": 12,
        "conversation_id": 1,
        "sender_id": 1,
        "text": "Sample message 12",
        "timestamp": datetime.now(),
        "status": "sent"
    }
]

blockchain = Blockchain()

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
    print(data)
    conversation_id = data["conversation_id"]
    message = data["Message"]
    sender_id = data["sender_id"]

    new_message = {
        "message_id": len(messages) + 1,
        "conversation_id": conversation_id,
        "sender_id": sender_id,
        "text": message,
        "timestamp": datetime.now(),
        "status": "sent"
    }

    messages.append(new_message)

    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.create_block(proof, previous_hash, [new_message])

    # Find participants
    participant_ids = next((c["participant_ids"] for c in conversations if c["conversation_id"] == conversation_id), [])

    # Rebuild the updated message list
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

    # Emit updated messages to all participants (you can refine this to emit per user)
    emit("chat_messages", {"messages": convo_messages}, broadcast=True)



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

@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/valid', methods=['GET'])
def valid():
    is_valid = blockchain.chain_valid(blockchain.chain)
    message = 'The Blockchain is valid.' if is_valid else 'The Blockchain is not valid.'
    return jsonify({'message': message}), 200

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5003)
