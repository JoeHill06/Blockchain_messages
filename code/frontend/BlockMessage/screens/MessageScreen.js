import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  SafeAreaView,
  FlatList,
} from 'react-native';
import { getChatMessages } from '../services/conversationServices';

class Message {
    constructor({ receiver_id, sender_id, message, timestamp, profile_url }) {
        this.reciever = receiver_id;
        this.sender = sender_id;
        this.message = message;
        this.timestamp = timestamp;
        this.profile_url = profile_url;
      }
}

export default function MessageScreen({ navigation, route }) {
    const {conversation_id,user_id, sender_id, sender_name, profileUrl } = route.params;
    const [search, setSearch] = useState('');
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        navigation.setOptions({ title: sender_name });
        const socket = getChatMessages(conversation_id, (data) => {
            console.log("Received data:", data);
            if (data && Array.isArray(data.messages)) {
                setMessages(data.messages);
            }
        });

        return () => socket.disconnect();
    }, [navigation, sender_name, conversation_id]);

    const renderItem = ({ item }) => (
      <View style={[
        styles.messageBubble,
        item.sender_id === user_id ? styles.sentMessage : styles.receivedMessage
      ]}>
        <Text style={styles.messageText}>{item.text}</Text>
        <Text style={styles.timestamp}>{item.timestamp}</Text>
      </View>
    );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
      </View>
      <FlatList
        data={messages}
        keyExtractor={(item, index) => index.toString()}
        renderItem={renderItem}
        contentContainerStyle={styles.listContent}
      />
      <TextInput
        style={styles.input}
        placeholder="Type a message..."
        value={search}
        onChangeText={setSearch}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  messageBubble: {
    padding: 10,
    marginVertical: 6,
    marginHorizontal: 12,
    backgroundColor: '#f0f0f0',
    borderRadius: 8,
  },
  sentMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#dcf8c6',
  },
  receivedMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#f0f0f0',
  },
  input: {
    padding: 10,
    borderTopWidth: 1,
    borderColor: '#ddd',
    backgroundColor: '#fff',
    marginHorizontal: 12,
    marginBottom: 10,
    borderRadius: 20,
  },
  timestamp: {
    fontSize: 10,
    color: '#888',
    textAlign: 'right',
    marginTop: 4,
  },
  header: {

    paddingBottom: 12,
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
  },
  messageText: {
    fontSize: 16,
    color: '#000',
  },

})
