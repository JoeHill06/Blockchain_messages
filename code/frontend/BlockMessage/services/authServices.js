// services/authService.js
export async function loginUser(username, password) {
    try {
      const response = await fetch('http://127.0.0.1:5003/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
  
      return await response.json();
    } catch (error) {
      throw new Error("Network error");
    }
  }