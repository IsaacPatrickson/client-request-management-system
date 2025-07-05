// === Utility: Resize SVG to match viewport ===
function updateViewBoxToViewport(svg) {
    const width = window.innerWidth;
    const height = window.innerHeight;
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.setAttribute('width', width);
    svg.setAttribute('height', height);
}

// === Easing Function (with optional delay at the beginning) ===
// Adds an initial "pause" using a delay before easing starts
function easeInOutCubic(t) {
    const delay = 0.4; // Portion of animation (0–1) to delay before easing
    if (t < delay) return 0;

    t = (t - delay) / (1 - delay); // Normalize `t` after delay
    return t < 0.5
        ? 4 * t * t * t                     // Ease in
        : 1 - Math.pow(-2 * t + 2, 3) / 2;  // Ease out
}

// === DOM References ===
const svg = document.getElementById('pieces');      // The root SVG element
const polygon1 = document.getElementById('path1');  // First polygon
const polygon2 = document.getElementById('path2');  // Second polygon

// === Animation State ===
let startTime = null;               // Time the animation starts
const duration = 1400;              // Total animation time (not directly used)
const delayPolygon2 = 300;          // Optional delay before polygon2 starts (unused in this version)
const pointDelays1 = [0, 600, 600, 600, 600];       // Delay per point for polygon1
const pointDelays2 = [0, 0, 400, 400, 400, 1000];   // Delay per point for polygon2
const durationPerPoint = 1000;      // How long each point takes to animate

// Point arrays used during interpolation
let currentPointsStart1 = [], currentPointsEnd1 = [];
let currentPointsStart2 = [], currentPointsEnd2 = [];

// === Helper Functions ===+
// === Interpolates each point of a polygon individually, with delay per point ===
function interpolatePointsWithDelays(pointsA, pointsB, elapsed, delays) {
    return pointsA.map((start, i) => {
        const end = pointsB[i];
        const delay = delays[i] || 0;

        // Calculate animation progress for this point
        let localT = (elapsed - delay) / durationPerPoint;
        localT = Math.max(0, Math.min(localT, 1));
        const easedT = easeInOutCubic(localT);

        // Interpolate between start and end
        const x = start[0] + (end[0] - start[0]) * easedT;
        const y = start[1] + (end[1] - start[1]) * easedT;
        return [x, y];
    });
}

// === Converts array of [x, y] points into SVG-compatible string ===
function pointsToString(points) {
    return points.map(p => p.join(',')).join(' ');
}

// === Main Animation Loop ===
function animate(timestamp) {
    if (!startTime) startTime = timestamp;
    const elapsed = timestamp - startTime;

    // Interpolate both polygons
    const interpolated1 = interpolatePointsWithDelays(currentPointsStart1, currentPointsEnd1, elapsed, pointDelays1);
    const interpolated2 = interpolatePointsWithDelays(currentPointsStart2, currentPointsEnd2, elapsed, pointDelays2);

    // Apply interpolated points to polygons
    polygon1.setAttribute('points', pointsToString(interpolated1));
    polygon2.setAttribute('points', pointsToString(interpolated2));

    // Stop when the longest delay + duration finishes
    const lastDelay = Math.max(
        ...pointDelays1,
        ...pointDelays2
    );

    if (elapsed < durationPerPoint + lastDelay) {
        requestAnimationFrame(animate);
    }
}

// === Set up the initial shapes and start the animation ===
function setupAndAnimate() {
    startTime = null;
    const width = window.innerWidth;
    const height = window.innerHeight;
    updateViewBoxToViewport(svg); // Ensure SVG matches screen size

    // Define initial and final shape for polygon1
    currentPointsStart1 = [
        [0, 0],
        [900, 550],
        [900, 550],
        [350, height],
        [0, height]
    ];

    currentPointsEnd1 = [
        [0, 0],
        [width, height],
        [width, height],
        [width, height],
        [0, height]
    ];

    // Define initial and final shape for polygon2
    currentPointsStart2 = [
        [0, 0],
        [450, 248],
        [1000, 550],
        [1000, 550],
        [400, height],
        [0, height]
    ];

    currentPointsEnd2 = [
        [0, 0],
        [width * 0.2, 0],
        [width * 0.70, height],
        [width * 0.70, height],
        [width * 0.70, height],
        [0, height]
    ];

    // Initialize starting shapes
    polygon1.setAttribute('points', pointsToString(currentPointsStart1));
    polygon2.setAttribute('points', pointsToString(currentPointsStart2));

    requestAnimationFrame(animate); // Kick off animation loop
}

// === Animate Again on Resize ===
function animateOnResize() {
    startTime = null;
    const width = window.innerWidth;
    const height = window.innerHeight;
    updateViewBoxToViewport(svg);

    // Read current polygon points as new starting points
    const parsePoints = el =>
        el.getAttribute('points')
            .trim()
            .split(' ')
            .map(pt => pt.split(',').map(Number));

    currentPointsStart1 = parsePoints(polygon1);
    currentPointsStart2 = parsePoints(polygon2);

    // Define new target shapes based on new size
    currentPointsEnd1 = [
        [0, 0],
        [width, height],
        [width, height],
        [width * 0.4, height],
        [0, height]
    ];

    currentPointsEnd2 = [
        [0, 0],
        [width * 0.2, 0],
        [width * 0.70, height],
        [width * 0.70, height],
        [width * 0.70, height],
        [0, height]
    ];

    // Re-run animation with new sizes
    requestAnimationFrame(animate);
}

// === Trigger animation on page load and resize ===
window.addEventListener('load', setupAndAnimate);
window.addEventListener('resize', animateOnResize);
