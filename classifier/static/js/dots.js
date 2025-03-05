const background = document.getElementById('background');
const numDots = 30; // Number of dots
const maxDistance = 100; // Maximum distance to connect dots

// Create random dots
let dots = [];
for (let i = 0; i < numDots; i++) {
  const dot = document.createElement('div');
  dot.classList.add('dot');
  dot.style.top = `${Math.random() * window.innerHeight}px`;
  dot.style.left = `${Math.random() * window.innerWidth}px`;
  background.appendChild(dot);
  dots.push({
    element: dot,
    x: parseFloat(dot.style.left),
    y: parseFloat(dot.style.top),
    vx: Math.random() * 2 - 1, // Random horizontal velocity
    vy: Math.random() * 2 - 1  // Random vertical velocity
  });
}

// Function to draw lines between dots
function drawLines() {
  const canvas = document.createElement('canvas');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  background.appendChild(canvas);
  const ctx = canvas.getContext('2d');
  
  // Clear the canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (let i = 0; i < dots.length; i++) {
    for (let j = i + 1; j < dots.length; j++) {
      const dot1 = dots[i];
      const dot2 = dots[j];
      const dist = Math.sqrt(Math.pow(dot1.x - dot2.x, 2) + Math.pow(dot1.y - dot2.y, 2));

      if (dist < maxDistance) {
        ctx.beginPath();
        ctx.moveTo(dot1.x, dot1.y);
        ctx.lineTo(dot2.x, dot2.y);
        ctx.strokeStyle = 'rgba(255, 255, 255, ' + (1 - dist / maxDistance) + ')';
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }
  }
}

// Function to update the position of dots
function updateDots() {
  dots.forEach(dot => {
    dot.x += dot.vx;
    dot.y += dot.vy;

    // Bounce off the walls
    if (dot.x <= 0 || dot.x >= window.innerWidth) dot.vx *= -1;
    if (dot.y <= 0 || dot.y >= window.innerHeight) dot.vy *= -1;

    // Update dot position
    dot.element.style.left = `${dot.x}px`;
    dot.element.style.top = `${dot.y}px`;
  });

  drawLines();
  requestAnimationFrame(updateDots);
}

// Start the animation
updateDots();
