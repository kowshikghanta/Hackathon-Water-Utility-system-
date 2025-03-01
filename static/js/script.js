async function fetchData() {
    const response = await fetch('/data');
    const data = await response.json();
    
    console.log("Fetched Data:", data);

    updateCharts(data);
    updateTable(data);
}

function updateTable(data) {
    const tableBody = document.getElementById("data-table-body");
    tableBody.innerHTML = "";

    data.forEach(row => {
        let tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${row.timestamp}</td>
            <td>${row.flow_rate.toFixed(2)}</td>
            <td>${row.water_level.toFixed(2)}</td>
        `;
        tableBody.appendChild(tr);
    });
}

function updateCharts(data) {
    let labels = data.map(row => row.timestamp);
    let flowRates = data.map(row => row.flow_rate);
    let waterLevels = data.map(row => row.water_level);

    let ctx = document.getElementById("sensorChart").getContext("2d");
    if (window.myChart) window.myChart.destroy();

    window.myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Flow Rate (L/min)',
                    data: flowRates,
                    borderColor: 'blue',
                    fill: false
                },
                {
                    label: 'Water Level (cm)',
                    data: waterLevels,
                    borderColor: 'green',
                    fill: false
                }
            ]
        }
    });
}

setInterval(fetchData, 2000);
fetchData();
