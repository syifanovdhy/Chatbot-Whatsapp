async function sendWhatsAppMessage(
    client,
    waId,
    message
) {

    try {

        if (!client.info) {

            console.log(
                "Client belum ready."
            );

            return false;
        }

        await client.sendMessage(
            waId,
            message
        );

        console.log(
            "Pesan berhasil dikirim."
        );

        return true;

    } catch (err) {

        console.log(err);

        return false;
    }
}

module.exports = {
    sendWhatsAppMessage
};