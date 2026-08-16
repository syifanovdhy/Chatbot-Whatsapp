let serviceChart = null;
let dailyChart = null;

async function loadStatistics() {

    const response = await fetch(
        "/dashboard/statistics"
    );

    const data = await response.json();

    console.log(data);

}
loadStatistics();

async function loadDashboard(period = "all") {

    const summaryResponse = await fetch(
        `/dashboard/summary?period=${period}`
    );

    const summary =
        await summaryResponse.json();

    document.getElementById(
        "total-users"
    ).innerText =
        summary.total_users;

    document.getElementById(
        "total-services"
    ).innerText =
        summary.total_services;

    const statisticsResponse = await fetch(
        `/dashboard/statistics?period=${period}`
    );

    const statistics =
        await statisticsResponse.json();

    renderServiceStatistics(
        statistics
    );

    renderServiceChart(
        statistics
    );

    const dailyResponse = await fetch(
        `/dashboard/daily-statistics?period=${period}`
    );

    const dailyData =
        await dailyResponse.json();

    renderDailyChart(
        dailyData
    );

    updateLastUpdated();
}

async function loadActiveConsultations() {

    const container = document.getElementById("active-consultations");

    try {
        const response = await fetch("/dashboard/consultations/active");
        const consultations = await response.json();

        container.innerHTML = "";

        if (consultations.length === 0) {
            container.innerText = "Tidak ada konsultasi aktif.";
            return;
        }

        consultations.forEach(consultation => {
            const item = document.createElement("article");
            item.className = "consultation-item";

            const details = document.createElement("div");
            details.className = "consultation-details";

            const title = document.createElement("h3");
            title.innerText = consultation.nama;

            const meta = document.createElement("p");
            meta.className = "consultation-meta";
            meta.innerText = `${consultation.wa_id} · ${consultation.agent_replied ? "Petugas sudah membalas" : "Menunggu petugas"}`;

            const need = document.createElement("p");
            need.innerText = `Keperluan: ${consultation.keperluan}`;

            const lastMessage = document.createElement("p");
            lastMessage.className = "consultation-last-message";
            lastMessage.innerText = `Pesan terakhir: ${consultation.last_message}`;

            details.append(title, meta, need, lastMessage);

            const finishButton = document.createElement("button");
            finishButton.className = "finish-button";
            finishButton.innerText = "Selesai";
            finishButton.addEventListener("click", () => finishConsultation(
                consultation.id,
                consultation.nama,
            ));

            item.append(details, finishButton);
            container.appendChild(item);
        });
    } catch (error) {
        container.innerText = "Gagal memuat konsultasi aktif.";
        console.error(error);
    }
}

async function finishConsultation(consultationId, userName) {

    if (!confirm(`Akhiri konsultasi dengan ${userName}?`)) {
        return;
    }

    const response = await fetch(
        `/dashboard/consultations/${consultationId}/finish`,
        { method: "POST" },
    );

    if (!response.ok) {
        alert("Konsultasi gagal ditutup.");
        return;
    }

    const result = await response.json();
    if (!result.notification_sent) {
        alert("Konsultasi ditutup, tetapi notifikasi WhatsApp gagal dikirim.");
    }

    loadDashboard(document.getElementById("period").value);
}

document.getElementById(
    "period"
).addEventListener(
    "change",
    function () {

        loadDashboard(
            this.value
        );

    }
);

loadActiveConsultations();
loadDashboard();

setInterval(() => {

    const period =
        document.getElementById(
            "period"
        ).value;

    loadDashboard(period);

}, 60000);

setInterval(loadActiveConsultations, 60000);

function renderServiceStatistics(
    statistics
) {

    const container =
        document.getElementById(
            "service-list"
        );

    container.innerHTML = "";

    statistics.forEach(item => {

        const row =
            document.createElement("div");

        row.className =
            "service-item";

        row.innerHTML = `
            <span class="service-name">
                ${item.menu}
            </span>

            <span class="service-count">
                ${item.jumlah}
            </span>
        `;

        container.appendChild(row);

    });
}

function renderServiceChart(statistics) {

    if (typeof Chart === "undefined") {
        console.warn("Chart.js tidak tersedia; grafik layanan tidak ditampilkan.");
        return;
    }

    const canvas =
        document.getElementById("service-chart");

    const labels = statistics.map(item => {

        switch (item.kode) {

            case "PERPUSTAKAAN":
                return "Perpustakaan";

            case "KONSULTASI":
                return "Konsultasi";

            case "SILASTIK":
                return "Silastik";

            case "ROMANTIK":
                return "Romantik";

            case "PENGADUAN":
                return "Pengaduan";

            default:
                return item.menu;
        }

    });

    const values = statistics.map(
        item => item.jumlah
    );

    if (serviceChart) {
        serviceChart.destroy();
    }

    serviceChart = new Chart(canvas, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [
                {
                    label: "Jumlah Layanan",

                    data: values
                }
            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            scales: {

                x: {
                    ticks: {
                        maxRotation: 0,
                        minRotation: 0
                    }
                },

                y: {
                    beginAtZero: true,

                    ticks: {
                        precision: 0
                    }
                }

            },

            plugins: {

                legend: {
                    display: false
                }

            }

        }

    });
}

function updateLastUpdated() {

    const now = new Date();

    document.getElementById(
        "last-updated"
    ).innerText = now.toLocaleString(
        "id-ID",
        {
            dateStyle: "medium",
            timeStyle: "short"
        }
    );
}

function renderDailyChart(data) {

    if (typeof Chart === "undefined") {
        console.warn("Chart.js tidak tersedia; grafik tren tidak ditampilkan.");
        return;
    }

    const canvas =
        document.getElementById("daily-chart");

    const labels = data.map(
        item => item.tanggal
    );

    const values = data.map(
        item => item.jumlah
    );

    if (dailyChart) {
        dailyChart.destroy();
    }

    dailyChart = new Chart(canvas, {

        type: "line",

        data: {

            labels: labels,

            datasets: [
                {
                    label: "Jumlah Layanan",
                    data: values,
                    tension: 0.3
                }
            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            scales: {

                y: {
                    beginAtZero: true,

                    ticks: {
                        precision: 0
                    }
                },

                x: {

                    ticks: {

                        maxRotation: 0,

                        minRotation: 0

                    }

                }

            }

        }

    });
}

function exportReport() {

    const period =
        document.getElementById(
            "period"
        ).value;

    window.location.href =
        `/dashboard/export?period=${period}`;
}


