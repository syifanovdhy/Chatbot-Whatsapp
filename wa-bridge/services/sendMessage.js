module.exports = function registerSendMessage(app, client) {

    app.post("/send-message", async (req, res) => {

        try {

            const { wa_id, message } = req.body;

            await client.sendMessage(
                wa_id,
                message
            );

            res.json({
                success: true
            });

        } catch (err) {

            console.log(err);

            res.status(500).json({
                success: false
            });

        }

    });

};