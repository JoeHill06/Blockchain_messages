# Blockchain-Secured Messaging App

This project is a real-time messaging application enhanced with blockchain technology to ensure message integrity and tamper-proof communication. The application allows users to send and receive messages through a socket-based real-time interface while storing message history on a custom-built Python blockchain.

## Overview

The purpose of this project is to demonstrate how blockchain technology can be used beyond cryptocurrency, specifically for secure and verifiable communication. It combines the practicality of modern web development (React Native + Flask + Socket.IO) with the theoretical security model of blockchain.

## Features

- Real-time messaging using Socket.IO
- User login and conversation switching
- Simulated users and chat data for demonstration
- Every message is written to a block and mined on the blockchain
- Blockchain is validated and auditable via dedicated endpoints
- Proof-of-work algorithm ensures blocks cannot be easily faked

## Tech Stack

### Frontend

- **React Native (Expo)**
  - Cross-platform mobile development
  - Realtime UI rendering with FlatList
  - Navigation stack for conversation switching

### Backend

- **Python (Flask)**
  - RESTful API for user login and conversation listing
  - Blockchain mining and validation logic
- **Socket.IO (Flask-SocketIO)**
  - WebSockets for real-time message sending and receiving

### Blockchain

- **Custom Python Blockchain**
  - Proof-of-work algorithm
  - SHA-256 fingerprinting of block data
  - JSON-based storage format
  - Chain validation logic

## Blockchain Architecture

Each block on the chain contains:
- `index`: the block's position
- `timestamp`: time the block was mined
- `proof`: proof of work computed from previous block
- `previous_hash`: SHA256 hash of the previous block
- `messages`: a list of messages mined into this block

### Message Integrity via Blockchain

- All messages are stored immutably in the blockchain.
- Each block is cryptographically linked to the previous using SHA-256.
- Any change to a message or block would invalidate the entire chain.
- A proof-of-work system ensures that mining new blocks requires computation, preventing easy tampering or forgery.

### Blockchain Endpoints

- `/get_chain`: Retrieve the full blockchain
- `/valid`: Check if the blockchain is valid and untampered

## Example Endpoints

- `POST /login`: Authenticate simulated users
- `POST /getUserConversations`: List available conversations
- Socket Events:
  - `get_messages`: Fetch conversation history
  - `send_message`: Send new message and mine it into blockchain

## Developer Skills Demonstrated

- Real-time application architecture using WebSockets
- Backend API development with Flask
- Blockchain architecture and cryptographic hashing
- Proof-of-work algorithm implementation
- State management and real-time UI with React Native
- Socket event handling and lifecycle control
- REST endpoint design and JSON serialization
- Secure design principles applied to message integrity

## How to Run the App

### Backend
1. Navigate to the backend directory.
2. Run the Flask server:
   ```bash
   python main.py
3. Run npm install to get react packagges from package.json
4. run pip install -r requirements.txt to get python packages
5. run npx expo start -c to start react native expo app

### How To Improve
1. make the blockchain decentralised from the backend server
2. increase security, including passwords
3. Create method for checking the blockchain is currenlty valid
