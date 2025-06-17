// contexts/AuthContext.js
import React, { createContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { loginUser } from '../services/authServices';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {

  useEffect(() => {
    AsyncStorage.getItem("LoginStatus").then((value) => {
      if (value === "true") {
        return true
      }
    });
  }, []);

  const login = async (username, password) => {
    const result = await loginUser(username, password);
    if (result.login === "success") {
      await AsyncStorage.setItem("LoginStatus", "true");
      return true;
    }
    return false;
  };

  const logout = async () => {
    await AsyncStorage.removeItem("LoginStatus");
  };

  return (
    <AuthContext.Provider value={{login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};