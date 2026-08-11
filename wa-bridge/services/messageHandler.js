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

        const contact = await message.getContact();

        const response = await sendMessageToBackend({
            wa_id: message.from,
            push_name: contact.pushname || "",
            message: message.body
        });
        
        if (response && response.reply) {
            await message.reply(response.reply);
        }

        // const contact = await message.getContact();

        console.log(contact.id);
        console.log(contact.number);
        console.log(contact.pushname);

    });

}

module.exports = registerMessageHandler;