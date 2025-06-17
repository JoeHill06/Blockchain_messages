import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
} from 'react-native';

import { getUserConversations } from '../services/conversationServices';

class Conversation {
  constructor({ username, lastMessage, timestamp }) {
    this.conversationName = username;
    this.lastMessage = lastMessage;
    this.timestamp = timestamp;
  }
}

export default function HomeScreen({ navigation }) {
  const [search, setSearch] = useState('');
  const [conversations, setConversations] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await getUserConversations();
        if (response?.conversations) {
          const mapped = response.conversations.map((item) =>
            new Conversation({
              username: item.partner_username,
              lastMessage: item.last_message,
              timestamp: new Date(item.last_updated).toLocaleTimeString(),
            })
          );
          setConversations(mapped);
        }
      } catch (error) {
        console.error("Failed to fetch conversations", error);
      }
    }
    fetchData();
  }, []);

  const filtered = conversations.filter(c =>
    c.conversationName.toLowerCase().includes(search.toLowerCase())
  );

  const renderItem = ({ item }) => (
    <TouchableOpacity style={styles.messageItem}>
      <View style={styles.textContainer}>
        <Text style={styles.name}>{item.conversationName}</Text>
        <Text style={styles.preview}>{item.lastMessage}</Text>
      </View>
      <Text style={styles.time}>{item.timestamp}</Text>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Messages</Text>
      </View>
      <TextInput
        style={styles.searchBar}
        placeholder="Search"
        value={search}
        onChangeText={setSearch}
      />
      <FlatList
        data={filtered}
        keyExtractor={(item, index) => index.toString()}
        renderItem={renderItem}
        contentContainerStyle={styles.listContent}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    paddingTop: 10,
    paddingBottom: 12,
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '700',
  },
  searchBar: {
    margin: 10,
    paddingHorizontal: 14,
    paddingVertical: 10,
    backgroundColor: '#f2f2f2',
    borderRadius: 10,
    fontSize: 16,
  },
  listContent: {
    paddingBottom: 20,
  },
  messageItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  textContainer: {
    flex: 1,
    paddingRight: 10,
  },
  name: {
    fontWeight: '600',
    fontSize: 16,
    marginBottom: 2,
  },
  preview: {
    fontSize: 14,
    color: '#555',
  },
  time: {
    fontSize: 12,
    color: '#888',
    alignSelf: 'flex-start',
  },
});