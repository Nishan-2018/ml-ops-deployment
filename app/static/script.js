document.getElementById('predictForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = document.getElementById('predictBtn');
    const resultContainer = document.getElementById('result');
    const loader = document.getElementById('loader');
    const content = document.getElementById('prediction-content');
    const predictionText = document.getElementById('prediction-text');

    // UI Loading State
    const originalBtnText = btn.querySelector('span').innerText;
    btn.querySelector('span').innerText = 'Calculating...';
    btn.disabled = true;

    resultContainer.classList.remove('hidden');
    loader.classList.remove('hidden');
    content.classList.add('hidden');

    // Gather data
    const data = {
        med_inc: parseFloat(document.getElementById('med_inc').value),
        house_age: parseFloat(document.getElementById('house_age').value),
        ave_rooms: parseFloat(document.getElementById('ave_rooms').value),
        population: parseFloat(document.getElementById('population').value)
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('Prediction failed');
        }

        const result = await response.json();

        // Format price as currency
        const formatter = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            maximumFractionDigits: 0
        });

        const formattedPrice = formatter.format(result.price);

        // Update UI
        setTimeout(() => {
            loader.classList.add('hidden');
            content.classList.remove('hidden');
            predictionText.innerText = formattedPrice;

            // Reset button
            btn.querySelector('span').innerText = originalBtnText;
            btn.disabled = false;
        }, 600); // Fake delay for smooth UX

    } catch (error) {
        console.error('Error:', error);
        loader.classList.add('hidden');
        content.classList.remove('hidden');
        predictionText.innerText = "Error";
        predictionText.style.color = "#ef4444";

        btn.querySelector('span').innerText = originalBtnText;
        btn.disabled = false;
    }
});
