let chart = null;

async function sendData(){

  // Reset UI
  document.getElementById("loader").style.display="block";
  document.getElementById("bar").style.width="0%";
  document.getElementById("result").innerHTML="";
  document.getElementById("reportBox").innerHTML="";

  document.getElementById("imageSection").style.display="none";
  document.getElementById("ctTitle").style.display="none";
  document.getElementById("ctImage").style.display="none";

  const dataSend={
    age:Number(age.value),
    years_smoking:Number(years.value),
    cigarettes_per_day:Number(perday.value),
    exercise:Number(exercise.value),
    pollution:Number(pollution.value)
  };

  const res = await fetch("http://127.0.0.1:8000/predict",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify(dataSend)
  });

  const data = await res.json();

  document.getElementById("loader").style.display="none";

  // Show text results
  document.getElementById("result").innerHTML =
    `Damage: ${data.damage_score}%<br><small>${data.explanation}</small>`;

  // Animate bar
  document.getElementById("bar").style.width = data.damage_score + "%";

  // Show images AFTER generation
  document.getElementById("imageSection").style.display="flex";
  document.getElementById("ctTitle").style.display="block";
  document.getElementById("ctImage").style.display="block";

  document.getElementById("healthyImg").src = "healthy.png?" + Date.now();
  document.getElementById("lungImage").src = "lung.png?" + Date.now();
  document.getElementById("ctImage").src = "lung_ct.png?" + Date.now();

  // Show medical report
  document.getElementById("reportBox").innerText = data.report;

  // Save history
  let history = JSON.parse(localStorage.getItem("history")||"[]");

  history.push({
    score:data.damage_score,
    time:new Date().toLocaleTimeString()
  });

  localStorage.setItem("history",JSON.stringify(history));

  drawChart();
}

function drawChart(){

  const history = JSON.parse(localStorage.getItem("history")||"[]");

  const labels = history.map(h=>h.time);
  const scores = history.map(h=>h.score);

  if(chart) chart.destroy();

  chart = new Chart(historyChart,{
    type:"line",
    data:{
      labels:labels,
      datasets:[{
        label:"Lung Damage %",
        data:scores,
        borderColor:"#3b82f6",
        tension:0.3
      }]
    }
  });
}
