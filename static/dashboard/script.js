async function loadStatistics() {

    const response = await fetch(
        "/dashboard/statistics"
    );

    const data = await response.json();

    console.log(data);

}


loadStatistics();

async function loadDashboard() {

    const summaryResponse = await fetch(
        "/dashboard/summary"
    );

    const summary =
        await summaryResponse.json();

    document.getElementById(
        "total-users"
    ).innerText = summary.total_users;

    document.getElementById(
        "total-services"
    ).innerText = summary.total_services;


    const statisticsResponse = await fetch(
        "/dashboard/statistics"
    );

    const statistics =
        await statisticsResponse.json();

    renderServiceStatistics(
        statistics
    );

}


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