export async function getUserConversations() {
    try {
        const response = await fetch('http://127.0.0.1:5003/getUserConversations', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
        });

        return await response.json();
    } catch (error) {
        throw new Error("Netwrok error")
    }
}



import { io } from "socket.io-client";

export const getChatMessages = (conversation_id, onMessageCallback) => {
  const socket = io("http://127.0.0.1:5003");

  socket.on("connect", () => {
    socket.emit("get_messages", { conversation_id });
  });

  socket.on("chat_messages", (data) => {
    onMessageCallback(data); // This should be an array of messages
  });

  socket.on("disconnect", () => {
    console.log("Socket disconnected");
  });

  socket.on("connect_error", (err) => {
    console.error("Socket connection error:", err.message);
  });

  return socket; // Return so you can disconnect later
};