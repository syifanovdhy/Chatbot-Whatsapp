const { Client, LocalAuth } =
    require("whatsapp-web.js");

const qrcode =
    require("qrcode-terminal");

const CLIENT_ID =
    process.env.CLIENT_ID || "pst-bot";

const client = new Client({

    authStrategy: new LocalAuth({
        clientId: CLIENT_ID
    }),

    puppeteer: {

        headless: true,

        // Use the locally installed Chrome when Puppeteer's downloaded cache
        // is unavailable (for example after this project is moved to a new PC).
        executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || undefined,

        args: [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage"
        ]

    }

});

client.on("qr", qr => {

    console.log("Scan QR");

    qrcode.generate(qr, {
        small: true
    });

});

client.on("ready", () => {

    console.log("=================================");
    console.log(" WhatsApp berhasil terhubung");
    console.log("=================================");

});

client.on("loading_screen", (percent, msg) => {

    console.log(percent, msg);

});

client.on("authenticated", () => {

    console.log("Authenticated");

});

client.on("auth_failure", msg => {

    console.log("Auth Failure");
    console.log(msg);

});

client.on("disconnected", reason => {

    console.log("Disconnected");
    console.log(reason);

});

module.exports = client;
