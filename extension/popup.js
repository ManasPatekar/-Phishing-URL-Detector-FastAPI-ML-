document.getElementById('check-url').addEventListener('click', async () => {
    try {
        let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        const url = tab.url;

        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ "url": url }),
        });

        if (!response.ok) throw new Error('Failed to fetch prediction');

        const result = await response.json();
        document.getElementById('result').innerText = `Prediction: ${result.prediction}`;
    } catch (error) {
        document.getElementById('result').innerText = `Error: ${error.message}`;
    }
});
