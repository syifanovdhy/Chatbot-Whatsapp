const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");

const client = new Client({
    authStrategy: new LocalAuth({
        clientId: "pst-bot"
    })
});

client.on("qr", (qr) => {
    console.log("Silakan scan QR berikut:");

    qrcode.generate(qr, {
        small: true
    });
});

client.on("ready", () => {
    console.log("=================================");
    console.log(" WhatsApp berhasil terhubung");
    console.log("=================================");
});

client.on("disconnected", (reason) => {

    console.log("WhatsApp terputus");

    console.log(reason);

});

module.exports = client;