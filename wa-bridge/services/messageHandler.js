const {
    sendMessageToBackend,
    sendDirectAgentReplyToBackend,
} = require("./api");
const {
    sendWhatsAppMessage,
    isAutomatedMessage,
} = require("./whatsappService");

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
            await sendWhatsAppMessage(
                client,
                message.from,
                response.reply
            );
        }

        // const contact = await message.getContact();

        console.log(contact.id);
        console.log(contact.number);
        console.log(contact.pushname);

    });

    client.on("message_create", async (message) => {

        if (!message.fromMe || !message.body) {
            return;
        }

        // Pesan yang dikirim API bot tidak boleh dicatat sebagai balasan petugas.
        if (isAutomatedMessage(message.to, message.body)) {
            return;
        }

        const response = await sendDirectAgentReplyToBackend({
            wa_id: message.to,
            message: message.body,
        });

        if (response && response.recorded) {
            console.log("Balasan petugas langsung dicatat:", response.consultation_id);
        }
    });

}

module.exports = registerMessageHandler;
