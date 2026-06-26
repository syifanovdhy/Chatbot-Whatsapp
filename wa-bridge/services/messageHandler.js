const { sendMessageToBackend } = require("./api");

function registerMessageHandler(client) {


    client.on("message", async (message) => {

        if (message.fromMe) {
            return;
        }

        if (!message.body) {
            return;
        }

        console.log("==========================");
        console.log("Pesan Baru");
        console.log("==========================");

        console.log("Dari :", message.from);
        console.log("Isi  :", message.body);

        const response = await sendMessageToBackend({
            user_id: 1,
            message: message.body
        });

        if (response && response.reply) {
            await message.reply(response.reply);
        }

    });

}

module.exports = registerMessageHandler;