let currentConsultationId = null;
let refreshInterval = null;

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
            ).innerText = consultation.nama;

            document.getElementById(
                "customer-instansi"
            ).innerText = consultation.instansi;

            currentConsultationId =
                consultation.id;

            loadTimeline(
                consultation.id
            );

            startAutoRefresh();

        };

        list.appendChild(item);

    });

}

loadConsultations();
setInterval(() => {

    loadConsultations();

},5000);

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

function startAutoRefresh(){

    if(refreshInterval){

        clearInterval(
            refreshInterval
        );

    }

    refreshInterval = setInterval(() => {

        if(currentConsultationId){

            loadTimeline(
                currentConsultationId
            );

        }

    },2000);

}

async function sendReply(){

    if(currentConsultationId == null){

        alert(
            "Pilih konsultasi terlebih dahulu."
        );

        return;

    }

    const textarea =
        document.getElementById(
            "reply-message"
        );

    const message =
        textarea.value.trim();

    if(message === ""){

        return;

    }

    await fetch(

        `/dashboard/consultations/${currentConsultationId}/reply`,

        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                message:message

            })

        }

    );

    textarea.value="";

    loadTimeline(
        currentConsultationId
    );

}