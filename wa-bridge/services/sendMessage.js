const {
    sendWhatsAppMessage
} = require("./whatsappService");

module.exports = function registerSendMessage(app, client) {

    app.post("/send-message", async (req, res) => {

        const {
            wa_id,
            message
        } = req.body;

        const success =
            await sendWhatsAppMessage(
                client,
                wa_id,
                message
            );

        if (success) {

            return res.json({
                success: true
            });

        }

        return res.status(500).json({
            success: false
        });

    });

};