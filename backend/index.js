async function loadSystemMetrics() {
    try {
        let response = await fetch("http://127.0.0.1:5000/api/metrics");
        let data = await response.json();

        if (!Array.isArray(data) || data.length === 0) return;

        let last = data[data.length - 1];

        document.getElementById("cpu").innerText = last.cpu + "%";
        document.getElementById("memory").innerText = last.memory + "%";
        document.getElementById("gpu").innerText = last.gpu + "%";

    } catch (e) {
        console.error("Error loading system metrics:", e);
    }
}


async function loadContainerMetrics() {
    try {
        let response = await fetch("    ");
        let data = await response.json();

        let containerList = document.getElementById("containers");
        containerList.innerHTML = "";

        for (let [name, stat] of Object.entries(data)) {
            containerList.innerHTML += `
                <h3>${name}</h3>
                <ul>
                    <li>CPU: ${stat.cpu}</li>
                    <li>Memory: ${stat.memory} / ${stat.memory_limit}</li>
                    <li>Network RX: ${stat.network_rx}</li>
                    <li>Network TX: ${stat.network_tx}</li>
                    <li>Status: ${stat.status}</li>
                </ul>
            `;
        }

    } catch (e) {
        console.error("Error loading container metrics:", e);
    }
}

loadSystemMetrics();
loadContainerMetrics();

