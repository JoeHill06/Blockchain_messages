export async function getUserConversations(username) {
    try {
        const response = await fetch('http://127.0.0.1:5003/getUserConversations', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username})
        });

        return await response.json();
    } catch (error) {
        throw new Error("Netwrok error")
    }
}