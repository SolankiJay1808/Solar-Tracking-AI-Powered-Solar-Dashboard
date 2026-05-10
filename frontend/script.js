const lightLabels = [];
const lightData = [];

const voltageLabels = [];
const voltageData = [];

// LIGHT CHART
const lightChart = new Chart(
    document.getElementById('lightChart'),
    {
        type: 'line',

        data: {
            labels: lightLabels,

            datasets: [{
                label: 'Light Intensity',

                data: lightData,

                borderWidth: 2
            }]
        },

        options: {
            responsive: true
        }
    }
);

// VOLTAGE CHART
const voltageChart = new Chart(
    document.getElementById('voltageChart'),
    {
        type: 'line',

        data: {
            labels: voltageLabels,

            datasets: [{
                label: 'Voltage',

                data: voltageData,

                borderWidth: 2
            }]
        },

        options: {
            responsive: true
        }
    }
);

async function fetchData(){

    try{

        const response = await fetch('http://127.0.0.1:5000/sensor-data');

        const data = await response.json();

        // UPDATE CARDS
        document.getElementById('ldrLeft').innerText = data.ldr_left;

        document.getElementById('ldrRight').innerText = data.ldr_right;

        document.getElementById('angle').innerText = data.servo_angle;

        document.getElementById('voltage').innerText =
            parseFloat(data.voltage).toFixed(2);
        document.getElementById('temperature').innerText =
    data.temperature + " °C";

document.getElementById('humidity').innerText =
    data.humidity + "%";

document.getElementById('weather').innerText =
    data.weather;

        // TIME LABEL
        const time = new Date().toLocaleTimeString();

        // LIGHT GRAPH
        lightLabels.push(time);

        lightData.push(data.ldr_left);

        // VOLTAGE GRAPH
        voltageLabels.push(time);

        voltageData.push(data.voltage);

        // LIMIT GRAPH POINTS
        if(lightLabels.length > 10){

            lightLabels.shift();
            lightData.shift();

            voltageLabels.shift();
            voltageData.shift();
        }

        // UPDATE CHARTS
        lightChart.update();

        voltageChart.update();

    }

    catch(error){

        console.log(error);
    }
}

fetchData();

setInterval(fetchData,1000);