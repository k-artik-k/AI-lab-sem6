console.log("✅ game.js loaded");

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

function draw(state) {
    console.log("Drawing state:", state);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Banana
    ctx.fillStyle = "yellow";
    ctx.beginPath();
    ctx.arc(state.banana.x, state.banana.y, 10, 0, Math.PI * 2);
    ctx.fill();

    // Box
    ctx.fillStyle = "brown";
    ctx.fillRect(state.box.x - 15, state.box.y - 15, 30, 30);

    // Monkey
    ctx.fillStyle = "black";
    ctx.beginPath();
    ctx.arc(state.monkey.x, state.monkey.y, 10, 0, Math.PI * 2);
    ctx.fill();

    if (state.has_banana) {
        alert("🎉 Monkey got the banana!");
    }
}

function update() {
    fetch("/state")
        .then(r => r.json())
        .then(draw);
}

function sendAction(action) {
    fetch("/action", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({move: action})
    })
    .then(r => r.json())
    .then(draw);
}

update();
