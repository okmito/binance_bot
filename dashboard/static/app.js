// app.js - client frontend for the minimal dashboard
const socket = io();
const priceValue = document.getElementById('priceValue');
const priceChange = document.getElementById('priceChange');
const lastUpdate = document.getElementById('lastUpdate');
const spark = document.getElementById('sparkline');
const ctx = spark.getContext('2d');

let history = [];

// simple sparkline renderer
function drawSpark() {
    const w = spark.width, h = spark.height;
    ctx.clearRect(0, 0, w, h);
    if (history.length === 0) return;
    const max = Math.max(...history), min = Math.min(...history);
    const range = Math.max(1, max - min);
    ctx.beginPath();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#06b6d4';
    history.forEach((v, i) => {
        const x = (i / (history.length - 1 || 1)) * w;
        const y = h - ((v - min) / range) * h;
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // draw last dot
    ctx.beginPath();
    ctx.fillStyle = '#0b69ff';
    const lastX = w;
    const lastY = h - ((history[history.length - 1] - min) / range) * h;
    ctx.arc(lastX - 2, lastY, 3, 0, Math.PI * 2);
    ctx.fill();
}

// update UI with a price object {symbol, price}
function updatePrice(data) {
    const p = parseFloat(data.price);
    if (isNaN(p)) return;
    const prev = history.length ? history[history.length - 1] : p;
    history.push(p);
    if (history.length > 40) history.shift();
    drawSpark();

    priceValue.textContent = p.toLocaleString('en-US', { maximumFractionDigits: 2 });
    const diff = (p - prev);
    const pct = prev ? (diff / prev * 100) : 0;
    priceChange.textContent = (diff >= 0 ? '+' : '') + diff.toFixed(2) + ` (${pct.toFixed(2)}%)`;
    priceChange.style.color = diff >= 0 ? '#059669' : '#dc2626';
    lastUpdate.textContent = new Date().toLocaleTimeString();
}

// default: socket emits mark_price events from server
socket.on('connect', () => {
    console.log('socket connected');
    document.getElementById('connectBtn').textContent = 'Connected';
});

socket.on('mark_price', (d) => {
    // d expected like {symbol, price}
    const normalized = { symbol: d.symbol || 'BTCUSDT', price: d.price || d.markPrice || d.p || d };
    updatePrice(normalized);
});

// form logic
const typeSelect = document.getElementById('type');
const priceRow = document.getElementById('priceRow');
typeSelect.addEventListener('change', e => {
    const v = e.target.value;
    if (v === 'LIMIT' || v === 'STOP_LIMIT' || v === 'OCO') priceRow.style.display = 'flex';
    else priceRow.style.display = 'none';
});

function fillExample(qty) {
    document.getElementById('quantity').value = qty;
    document.getElementById('side').value = 'BUY';
    document.getElementById('type').value = 'MARKET';
    priceRow.style.display = 'none';
}

function subscribeSymbol() {
    alert('Server subscribes by default. Use the REPL or console to change symbol subscription on server side.');
}

// Place order / dry-run logic via POST to server endpoint
const orderForm = document.getElementById('orderForm');
const orderResult = document.getElementById('orderResult');
const dryRunBtn = document.getElementById('dryRunBtn');

function collectForm() {
    return {
        symbol: document.getElementById('symbol').value,
        side: document.getElementById('side').value,
        type_: document.getElementById('type').value,
        quantity: document.getElementById('quantity').value,
        price: document.getElementById('price').value || undefined,
        stopPrice: document.getElementById('stopPrice').value || undefined
    };
}

orderForm.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const data = collectForm();
    orderResult.textContent = 'Sending...';
    try {
        const resp = await fetch('/place_order', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        const j = await resp.json();
        orderResult.textContent = JSON.stringify(j, null, 2);
    } catch (err) {
        orderResult.textContent = 'Error: ' + err;
    }
});

dryRunBtn.addEventListener('click', async () => {
    const data = collectForm();
    data.dryRun = true;
    orderResult.textContent = 'Dry-run...';
    try {
        const resp = await fetch('/place_order', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        const j = await resp.json();
        orderResult.textContent = JSON.stringify(j, null, 2);
    } catch (err) {
        orderResult.textContent = 'Error: ' + err;
    }
});
