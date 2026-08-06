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

        list.appendChild(item);

    });

}

loadConsultations();

async function loadTimeline(id){

    const response = await fetch(

        `/dashboard/consultations/${id}/timeline`

    );

    const data = await response.json();

    console.log(data);

}

item.onclick = () => {

    loadTimeline(
        consultation.id
    );

};