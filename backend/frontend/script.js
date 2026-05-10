async function fetchData(){

    const response = await fetch('http://127.0.0.1:5000/sensor-data');

    const data = await response.json();

    document.getElementById('ldrLeft').innerText = data.ldr_left;

    document.getElementById('ldrRight').innerText = data.ldr_right;

    document.getElementById('angle').innerText = data.servo_angle;

    document.getElementById('voltage').innerText = data.voltage;
}

setInterval(fetchData, 1000);