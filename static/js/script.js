async function fetchData() {
    const response = await fetch('/data');
    const data = await response.json();
    updateCharts(data);
}

function updateCharts(data) {
    let labels = data.map(entry => entry.timestamp);
    let flowRates = data.map(entry => entry.flow_rate);
    let levels = data.map(entry => entry.water_level);
    
    let ctx1 = document.getElementById("flowChart").getContext("2d");
    new Chart(ctx1, { type: "line", data: { labels, datasets: [{ label: "Flow Rate", data: flowRates }] } });

    let ctx2 = document.getElementById("levelChart").getContext("2d");
    new Chart(ctx2, { type: "line", data: { labels, datasets: [{ label: "Water Level", data: levels }] } });
}
fetch('/data')
    .then(response => response.json())
    .then(data => {
        console.log("Received Data:", data); 
    })
    .catch(error => console.error("Error fetching data:", error));

setInterval(fetchData, 2000);
