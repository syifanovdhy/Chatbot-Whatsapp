const axios = require ("axios");
const { FASTAPI_URL } = require ("../config");

async function sendMessageToBackend(payload) {
    try {
        const response = await axios.post(
            `${FASTAPI_URL}/chat`,
            payload
        );
        return response.data;
    } catch (error) {
        console.error("Error sending message to backend:");

        if (error.response) {
            console.error("Response error:", error.response.data);
        } else {
            console.error("Request error:", error.message);
        }
        
        return null;
    }
}

async function sendDirectAgentReplyToBackend(payload) {
    try {
        const response = await axios.post(
            `${FASTAPI_URL}/agent/direct-reply`,
            payload
        );
        return response.data;
    } catch (error) {
        console.error("Error recording direct agent reply:", error.message);
        return null;
    }
}

module.exports = { 
    sendMessageToBackend,
    sendDirectAgentReplyToBackend,
};
