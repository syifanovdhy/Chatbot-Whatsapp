const automatedMessages = new Set();

function messageKey(waId, message) {
    return `${waId}|${message}`;
}

function markAutomatedMessage(waId, message) {
    const key = messageKey(waId, message);
    automatedMessages.add(key);
    setTimeout(() => automatedMessages.delete(key), 60_000);
}

function isAutomatedMessage(waId, message) {
    const key = messageKey(waId, message);
    if (!automatedMessages.has(key)) {
        return false;
    }

    automatedMessages.delete(key);
    return true;
}

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

        markAutomatedMessage(waId, message);

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
    sendWhatsAppMessage,
    isAutomatedMessage,
};
