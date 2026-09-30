// ==========================================
// SMART AGRICULTURE - MAIN JAVASCRIPT
// ==========================================


// ------------------------------------------
// Weather API
// ------------------------------------------

async function getWeather() {

    const status = document.getElementById("weather-status");

    if (!status) {
        return;
    }

    status.innerText = "⏳ Getting current weather...";

    try {

        const response = await fetch("/api/weather");

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Unable to get weather data"
            );
        }

        const temperature =
            document.getElementById("temperature");

        const humidity =
            document.getElementById("humidity");

        const rainfall =
            document.getElementById("rainfall");


        if (temperature) {
            temperature.value = data.temperature;
        }

        if (humidity) {
            humidity.value = data.humidity;
        }

        if (rainfall) {
            rainfall.value = data.rainfall;
        }


        status.innerText =
            "✅ Weather data loaded automatically.";

    }

    catch (error) {

        console.error("Weather Error:", error);

        status.innerText =
            "❌ " + error.message;

    }
}


// ------------------------------------------
// Image Preview
// ------------------------------------------

function previewImage(event) {

    const image =
        document.getElementById("image-preview");

    const container =
        document.getElementById("preview-container");

    if (!image || !container) {
        return;
    }

    const file =
        event.target.files[0];

    if (file) {

        image.src =
            URL.createObjectURL(file);

        container.style.display =
            "block";

    }

}


// ------------------------------------------
// Page Loaded
// ------------------------------------------

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "Smart Agriculture JavaScript loaded successfully."
        );

    }
);