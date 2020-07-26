
// Function to get a new date every time so it doesn't go stale
function currentDate(){
  var d = new Date();
  var date_today = "";
  date_today = d.getFullYear() + "-" + d.getMonth() + "-" + d.getDate();
  return date_today
}

// Get average for last week
function weekAverage(){
  console.log("Getting week average");
  var backd = new Date();
  var week_points = [];
  var week_sum = 0;
  for (let i=0; i < 6; i++) {
    backd.setDate(d.getDate() - i);
    var date_past = "";
    var past_points = 0;
    date_past = backd.getFullYear() + "-" + backd.getMonth() + "-" + backd.getDate();
    console.log("Checking date: " + date_past);
    past_points = localStorage.getItem(date_past) || 0;
    if (past_points > 0) {
      week_points.push(past_points);
      console.log("Adding: " + past_points);
      week_sum = parseInt(week_sum) + parseInt(past_points);
    }
  }
  if (week_points.length > 0) {
    return week_sum / week_points.length;
  } else {
    return 0;
  }
}

function getToday(){
  //console.log(typeof localStorage.getItem(currentDate()));
  var crt = 0;
  crt = localStorage.getItem(currentDate()) || 0;
  return parseInt(crt);
}

function addPoints(){
  let points = parseInt(document.getElementById('ptsInput').value);
  let current = getToday();
  if (Number.isInteger(points) && Number.isInteger(current)) {
    console.log("Current:" + current + " Key: " + currentDate() + " Value: " + (points + current));
    document.getElementById('added').innerHTML = points;
    document.getElementById('ptsInput').value = null;
    localStorage.setItem(currentDate(), (points + current));
    displayValues();
  } else {
    console.log("points: " + points + ", current: " + current);
  }
};

function removePoints(){
  let points = parseInt(document.getElementById('ptsInput').value);
  let current = getToday();
  if (Number.isInteger(points) && Number.isInteger(current)) {
    console.log("Current:" + current + " Key: " + currentDate() + " Value: " + (points + current));
    document.getElementById('added').innerHTML = "-" + points;
    document.getElementById('ptsInput').value = null;
    localStorage.setItem(currentDate(), (current - points));
    displayValues();
  }
};

function displayValues(){
  console.log("Displaying values");
  document.getElementById('total').innerHTML = getToday();
  document.getElementById('avg').innerHTML = weekAverage();
}

displayValues();
document.getElementById("btnAdd").addEventListener("click", addPoints)
document.getElementById("btnRem").addEventListener("click", removePoints)
