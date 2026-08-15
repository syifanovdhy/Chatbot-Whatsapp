let serviceChart = null;

async function loadStatistics() {

    const response = await fetch(
        "/dashboard/statistics"
    );

    const data = await response.json();

    console.log(data);

}


loadStatistics();

async function loadDashboard(
    period = "all"
) {

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

loadDashboard();

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