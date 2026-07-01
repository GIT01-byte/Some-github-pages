const day = document.getElementById("day");
const hrs = document.getElementById("hrs");
const min = document.getElementById("min");
const sec = document.getElementById("sec");

const currentYear = new Date().getFullYear();
console.log(currentYear);

const newYear = new Date(`1 Jan ${currentYear + 1} 00:00:00`);
console.log(newYear);

function countodownTimer() {
  const todayDate = Date.now();
  console.log(todayDate);

  // Разница между текущей датой и Новым Годом
  const gap = newYear - todayDate;
  console.log(gap);

  const d = Math.floor(gap / 1000 / 60 / 60 / 24);
  const h = Math.floor((gap / 1000 / 60 / 60) % 24);
  const m = Math.floor((gap / 1000 / 60) % 60);
  const s = Math.floor((gap / 1000) % 60);

  day.innerHTML = d
  hrs.innerHTML = h
  min.innerHTML = m
  sec.innerHTML = s
}

setInterval(countodownTimer, 1000);
