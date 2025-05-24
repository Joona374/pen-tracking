const canvas = document.getElementById('canvas');
const ctx = canvas.getContext("2d")

let color = "red"

const redButton = document.getElementById("button-red")
redButton.addEventListener("click", (event) => {
    color = "red"
})

const greenButton = document.getElementById("button-green")
greenButton.addEventListener("click", (event) => {
    color = "green"
})

const blueButton = document.getElementById("button-blue")
blueButton.addEventListener("click", (event) => {
    color = "blue"
})


let mouseX = 0;
let mouseY = 0;

ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight * 0.9;



window.addEventListener("mousemove", (event) => {
    mouseX = event.clientX;
    mouseY = event.clientY;
})

function drawDot(x, y) {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.beginPath();
    ctx.arc(x, y, 15, 0, Math.PI * 2)
    ctx.fillStyle = color;
    ctx.fill();
}

function animate() {
    drawDot(mouseX, mouseY);
    requestAnimationFrame(animate);

}

animate();