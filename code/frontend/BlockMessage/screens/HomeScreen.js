import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  RefreshControl,
  Image
} from 'react-native';

import { getUserConversations } from '../services/conversationServices';

class Conversation {
  constructor({ conversation_id, username,user_id, partner_user_id, lastMessage, timestamp, profile_url }) {
    this.conversation_id = conversation_id;
    this.conversationName = username;
    this.user_id = user_id;
    this.other_user_id = partner_user_id;
    this.lastMessage = lastMessage;
    this.timestamp = timestamp;
    this.profile_url = profile_url;
  }
}

export default function HomeScreen({ navigation }) {
  const [search, setSearch] = useState('');
  const [conversations, setConversations] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = async () => {
    try {
      const response = await getUserConversations();
      if (response?.conversations) {
        const mapped = response.conversations.map((item) =>
          new Conversation({
            conversation_id: item.conversation_id,
            user_id: item.user_id,
            sender_id: item.other_user_id,
            username: item.partner_username,
            lastMessage: item.last_message,
            timestamp: new Date(item.last_updated).toLocaleTimeString(),
            profile_url: item.partner_profile_url, 
          })
        );
        setConversations(mapped);
      }
    } catch (error) {
      console.error("Failed to fetch conversations", error);
    }
  };

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    fetchData().then(() => setRefreshing(false));
  }, []);

  useEffect(() => {
    fetchData();
  }, []);

  const filtered = conversations.filter(c =>
    c.conversationName.toLowerCase().includes(search.toLowerCase())
  );

  const renderItem = ({ item }) => {
    
    return (
      <TouchableOpacity
        style={styles.messageItem}
        onPress={() =>
          navigation.navigate('MessageScreen', {
            conversation_id: item.conversation_id,
            sender_id: item.other_user_id,
            user_id: item.user_id,
            sender_name: item.conversationName,
            profileUrl: item.profile_url
          })
        }
      >
        <View style={styles.textContainer}>
          <Image source={{ uri: item.profile_url }} style={styles.avatar} />
          <Text style={styles.name}>{item.conversationName}</Text>
          <Text style={styles.preview}>{item.lastMessage}</Text>
        </View>
        <Text style={styles.time}>{item.timestamp}</Text>
      </TouchableOpacity>
    );
  };

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
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
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
  avatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    marginRight: 10,
  }
});