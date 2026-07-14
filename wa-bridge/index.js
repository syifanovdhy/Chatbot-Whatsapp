const client = require("./services/whatsapp");
const registerMessageHandler = require("./services/messageHandler");

const app = require("./server");

const registerSendMessage = require("./services/sendMessage");

console.log("=================================");
console.log("   PST WhatsApp Bridge Starting");
console.log("=================================");

registerMessageHandler(client);
registerSendMessage(app, client);

app.listen(3000, () => {

    console.log(
        "Node API running on port 3000"
    );

});

client.initialize();
