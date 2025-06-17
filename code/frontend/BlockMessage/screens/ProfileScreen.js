import { AuthContext } from '../contexts/AuthContext';
import React,{ useContext } from 'react';
import { View, Text, Button, Alert, StyleSheet } from 'react-native';


export default function ProfileScreen({ navigation }) {
  const { logout } = useContext(AuthContext);
  return (
    <View style={styles.container}>
      <Text>Profile</Text>
      <Button title="Go to Login" onPress={() => navigation.navigate('Login')} />
      <Button
        title="Logout"
        onPress={() => {
          logout();
          navigation.navigate('Login');
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center', 
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
  },
});