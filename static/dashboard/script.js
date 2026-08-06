let currentConsultationId = null;

async function loadConsultations() {

    const response = await fetch(
        "/dashboard/consultations"
    );

    const data = await response.json();

    const list = document.getElementById(
        "consultation-list"
    );

    list.innerHTML = "";

    data.forEach(consultation => {

        const item = document.createElement("div");

        item.className = "consultation-item";

        item.innerHTML = `
            <strong>${consultation.nama}</strong><br>
            <small>${consultation.instansi}</small>
        `;

        item.onclick = () => {

            document.getElementById(
                "customer-name"
            ).innerText =
                consultation.nama;

            document.getElementById(
                "customer-instansi"
            ).innerText =
                consultation.instansi;

            loadTimeline(
                consultation.id
            );

        };

        list.appendChild(item);

    });

}

loadConsultations();

async function loadTimeline(id){

    currentConsultationId = id;

    const response = await fetch(

        `/dashboard/consultations/${id}/timeline`

    );

    const timeline = await response.json();

    const chatBox = document.getElementById(
        "chat-box"
    );

    chatBox.innerHTML = "";

    timeline.forEach(item => {

        const bubble = document.createElement("div");

        if(item.type === "message"){

            bubble.className =
                item.sender === "user"
                ? "bubble user"
                : "bubble agent";

            bubble.innerHTML = item.content;

        }

        else{

            bubble.className = "activity";

            bubble.innerHTML =
                item.description;

        }

        chatBox.appendChild(
            bubble
        );

    });

}