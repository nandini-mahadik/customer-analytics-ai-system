async function predictPurchase() {
    const data = {
        Recency: parseFloat(document.getElementById("recency").value),
        Frequency: parseFloat(document.getElementById("freq").value),
        Monetary: parseFloat(document.getElementById("monetary").value),
        Avg_Order_Value: parseFloat(document.getElementById("avg").value)
    };

    console.log("Sending data:", data); // DEBUG

    const response = await fetch("http://127.0.0.1:5000/predict_purchase", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    console.log("Response:", result); // DEBUG

    const el = document.getElementById("purchaseResult");

    el.innerText = result.message + " (Prob: " + result.probability.toFixed(2) + ")";
    el.className = "result " + (result.prediction === 1 ? "success" : "danger");
}
async function predictChurn() {
    const data = {
        Recency: parseFloat(document.getElementById("recency").value),
        Frequency: parseFloat(document.getElementById("freq").value),
        Monetary: parseFloat(document.getElementById("monetary").value),
        Avg_Order_Value: parseFloat(document.getElementById("avg").value)
    };

    const response = await fetch("http://127.0.0.1:5000/predict_churn", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    const el = document.getElementById("churnResult");

    el.innerText = result.message + " (Prob: " + result.probability.toFixed(2) + ")";
    el.className = "result " + (result.prediction === 1 ? "danger" : "success");
}