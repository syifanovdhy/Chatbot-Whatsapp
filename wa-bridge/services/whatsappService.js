async function sendWhatsAppMessage(client, waId, message) {

    try {

        await client.sendMessage(
            waId,
            message
        );

        console.log("=================================");
        console.log("Pesan berhasil dikirim");
        console.log("Tujuan :", waId);
        console.log("=================================");

        return true;

    } catch (err) {

        console.error(err);

        return false;

    }

}

module.exports = {
    sendWhatsAppMessage
};