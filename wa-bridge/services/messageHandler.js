function registerMessageHandler(client) {

    client.on("message", async (message) => {

        console.log("==========================");
        console.log("Pesan Baru");
        console.log("==========================");

        console.log("Dari :", message.from);
        const contact = await message.getContact();
        console.log(contact.pushname);
        console.log("Isi  :", message.body);

    });

}

module.exports = registerMessageHandler;