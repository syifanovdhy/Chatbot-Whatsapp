const client = require("./services/whatsapp");

console.log("TYPE CLIENT :", typeof client);
console.log(
    "HAS ON      :",
    typeof client.on
);

const registerMessageHandler =
    require("./services/messageHandler");

const app = require("./server");

const registerSendMessage =
    require("./services/sendMessage");


console.log("=================================");
console.log("   PST WhatsApp Bridge Starting");
console.log("=================================");

registerMessageHandler(client);

registerSendMessage(
    app,
    client
);

const PORT =
    process.env.PORT || 3000;

app.listen(PORT, () => {

    console.log(
        `Node API running on port ${PORT}`
    );

});

client.initialize();