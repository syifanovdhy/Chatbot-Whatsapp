const client = require("./services/whatsapp");
const registerMessageHandler = require("./services/messageHandler");

console.log("=================================");
console.log("   PST WhatsApp Bridge Starting");
console.log("=================================");

registerMessageHandler(client);

client.initialize();

