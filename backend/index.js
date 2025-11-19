async function loadMetrics() {
    try {
        let response = await fetch("http://127.0.0.1:5001/api/metrics");
        let data = await response.json();

        document.getElementById("cpu").innerText = data.cpu;
        document.getElementById("memory").innerText = data.memory;
        document.getElementById("gpu").innerText = data.gpu;

    } catch (err) {
        console.error("API error:", err);
    }
}

loadMetrics();
