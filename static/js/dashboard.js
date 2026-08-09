// =============================================================================
// static/js/dashboard.js
// Optimized K-Means Dashboard JavaScript
// COVID Data Analysis & Visualization Flask Application
// =============================================================================

let scatterChartInstance    = null;
let distChartInstance       = null;
let movingAvgChartInstance  = null;
let correlationChartInstance = null;
let bubbleChartInstance     = null;

const colors = [
    '#0d6efd', // Blue
    '#198754', // Green
    '#ffc107', // Yellow
    '#dc3545', // Red
    '#6f42c1', // Purple
    '#fd7e14'  // Orange
];

document.addEventListener("DOMContentLoaded", () => {
    const scatterCanvas = document.getElementById("kmeansScatterChart");
    if (scatterCanvas) {
        console.log("K-Means Dashboard Initialized");
        loadKMeansDashboard();

        const refreshBtn = document.getElementById("refreshKMeansBtn");
        if (refreshBtn) {
            refreshBtn.addEventListener("click", () => {
                loadKMeansDashboard();
            });
        }
    }

    // Load additional charts
    if (document.getElementById("movingAvgChart"))  loadMovingAvgChart();
    if (document.getElementById("correlationChart")) loadCorrelationChart();
    if (document.getElementById("bubbleChart"))      loadBubbleChart();
});

async function loadKMeansDashboard() {
    try {
        showLoader();
        const data = await fetchKMeansData();
        
        updateKPIs(data);
        renderScatterChart(data);
        renderDistChart(data);
        updateInsights(data);
        
        hideLoader();
    } catch (error) {
        console.error("Error loading K-Means Dashboard:", error);
        hideLoader();
    }
}

async function fetchKMeansData() {
    const response = await fetch("/api/kmeans");
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

function updateKPIs(data) {
    const totalRecords = document.getElementById("insightTotalRecords");
    if (totalRecords) totalRecords.innerText = Number(data.total_records).toLocaleString();
    const numClusters = document.getElementById("insightNumClusters");
    if (numClusters) numClusters.innerText = data.n_clusters;
    const silScore = document.getElementById("insightSilhouetteScore");
    if (silScore) silScore.innerText = data.sil_score;
}

function renderScatterChart(data) {
    const ctx = document.getElementById("kmeansScatterChart").getContext("2d");
    
    if (scatterChartInstance) {
        scatterChartInstance.destroy();
    }
    
    // Group points by cluster
    const clusterGroups = {};
    for (let i = 0; i < data.n_clusters; i++) {
        clusterGroups[i] = [];
    }
    
    data.points.forEach(p => {
        if (clusterGroups[p.cluster]) {
            clusterGroups[p.cluster].push({
                x: p.x,
                y: p.y,
                country: p.country,
                date: p.date
            });
        }
    });
    
    const datasets = [];
    
    // Add cluster points
    for (let i = 0; i < data.n_clusters; i++) {
        datasets.push({
            label: `Cluster ${i}`,
            data: clusterGroups[i],
            backgroundColor: colors[i % colors.length] + '80', // Add transparency
            borderColor: colors[i % colors.length],
            borderWidth: 1,
            pointRadius: 4,
            pointHoverRadius: 6
        });
    }
    
    // Add Centroids
    datasets.push({
        label: 'Centroids',
        data: data.centroids.map(c => ({ x: c.x, y: c.y })),
        backgroundColor: '#000000',
        borderColor: '#ffffff',
        borderWidth: 2,
        pointRadius: 10,
        pointHoverRadius: 12,
        pointStyle: 'rectRot' // Rotating rectangle (diamond)
    });
    
    scatterChartInstance = new Chart(ctx, {
        type: 'scatter',
        data: { datasets: datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const point = context.raw;
                            if (context.dataset.label === 'Centroids') {
                                return `Centroid: Cases = ${point.x.toFixed(1)}, Deaths = ${point.y.toFixed(1)}`;
                            }
                            return `${point.country} (${point.date}) - Cases: ${point.x.toLocaleString()}, Deaths: ${point.y.toLocaleString()}`;
                        }
                    }
                },
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 15
                    }
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Daily New Cases',
                        font: { weight: 'bold' }
                    },
                    grid: { display: false }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Daily New Deaths',
                        font: { weight: 'bold' }
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

function renderDistChart(data) {
    const canvas = document.getElementById("kmeansDistChart");
    if (!canvas) return; // Exit safely if the chart element is not present
    
    const ctx = canvas.getContext("2d");
    
    if (distChartInstance) {
        distChartInstance.destroy();
    }
    
    // Limit to top 5 clusters
    const topClusters = data.distribution.slice(0, 5);
    
    distChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: topClusters.map(d => `Cluster ${d.cluster}`),
            datasets: [{
                data: topClusters.map(d => d.count),
                backgroundColor: topClusters.map(d => colors[d.cluster % colors.length] + 'c0'),
                borderColor: topClusters.map(d => colors[d.cluster % colors.length]),
                borderWidth: 1,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y', // Horizontal bars
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Record Count',
                        font: { weight: 'bold' }
                    }
                },
                y: {
                    grid: { display: false }
                }
            }
        }
    });
}

// Ensure the theme toggling works by carrying over any loader calls
function updateInsights(data) {
    const largestEl = document.getElementById("insightLargestCluster");
    if (largestEl) largestEl.innerHTML = `Cluster <strong>${data.insights.largest_cluster}</strong> is the most dominant cluster.`;
    
    const smallestEl = document.getElementById("insightSmallestCluster");
    if (smallestEl) smallestEl.innerHTML = `Cluster <strong>${data.insights.smallest_cluster}</strong> is the smallest cluster.`;
    
    const balanceSpan = document.getElementById("insightBalanceStatus");
    if (balanceSpan) {
        if (data.insights.balance === "balanced") {
            balanceSpan.innerHTML = `<span class="badge bg-success">Balanced</span> Distribution is relatively even.`;
        } else {
            balanceSpan.innerHTML = `<span class="badge bg-warning text-dark">Imbalanced</span> Significant size disparities between clusters.`;
        }
    }
    
    const interpEl = document.getElementById("insightInterpretation");
    if (interpEl) interpEl.innerText = data.insights.interpretation;
}

function showLoader() {
    const loader = document.getElementById("loader");
    if (loader) {
        loader.style.display = "flex";
    }
}

function hideLoader() {
    const loader = document.getElementById("loader");
    if (loader) {
        loader.style.display = "none";
    }
}

// =============================================================================
// COUNTRY SELECTOR LOGIC
// =============================================================================

// Global defaults stored from initial server render
const globalDefaults = {
    cases: document.getElementById("valCases")?.innerText || "—",
    deaths: document.getElementById("valDeaths")?.innerText || "—",
    tests: document.getElementById("valTests")?.innerText || "—",
    countries: document.getElementById("valCountries")?.innerText || "—"
};

document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById("countrySelect");
    const resetBtn = document.getElementById("resetCountryBtn");
    const badge = document.getElementById("selectedCountryBadge");
    const badgeName = document.getElementById("selectedCountryName");

    if (!select) return;

    select.addEventListener("change", async () => {
        const country = select.value;

        if (country === "global") {
            resetToGlobal();
            return;
        }

        // Show reset button + badge
        resetBtn?.classList.remove("d-none");
        badge?.classList.remove("d-none");
        if (badgeName) badgeName.textContent = country;

        // Animate cards out
        setCardOpacity(0.4);

        try {
            const res = await fetch(`/api/country/${encodeURIComponent(country)}`);
            if (!res.ok) throw new Error("Country data unavailable");
            const data = await res.json();

            // Compute aggregated totals
            const totalCases  = data.cases.reduce((a, b) => a + b, 0);
            const totalDeaths = data.deaths.reduce((a, b) => a + b, 0);
            const totalTests  = data.tests.reduce((a, b) => a + b, 0);
            const dateFrom    = data.dates[0] || "—";
            const dateTo      = data.dates[data.dates.length - 1] || "—";

            // Update card values
            setText("valCases",     formatNum(totalCases));
            setText("valDeaths",    formatNum(totalDeaths));
            setText("valTests",     formatNum(totalTests));
            setText("valCountries", `${dateFrom} → ${dateTo}`);

            // Update card labels
            setText("labelCases",     "Total Cases");
            setText("labelDeaths",    "Total Deaths");
            setText("labelTests",     "Total Tests");
            setText("labelCountries", "Date Range");

            // Update section heading
            setText("summaryTitle",    `${country} — COVID-19 Summary`);
            setText("summarySubtitle", `Cumulative statistics for ${country} from ${dateFrom} to ${dateTo}.`);

        } catch (err) {
            console.error("Country fetch error:", err);
            setText("valCases",     "N/A");
            setText("valDeaths",    "N/A");
            setText("valTests",     "N/A");
            setText("valCountries", "No data");
        }

        // Animate cards back in
        setCardOpacity(1);
    });

    resetBtn?.addEventListener("click", () => {
        select.value = "global";
        resetToGlobal();
    });

    function resetToGlobal() {
        setCardOpacity(0.4);

        // Restore global values
        setText("valCases",     globalDefaults.cases);
        setText("valDeaths",    globalDefaults.deaths);
        setText("valTests",     globalDefaults.tests);
        setText("valCountries", globalDefaults.countries);

        // Restore labels
        setText("labelCases",     "Total New Cases");
        setText("labelDeaths",    "Total New Deaths");
        setText("labelTests",     "Total Tests");
        setText("labelCountries", "Countries Tracked");

        // Restore heading
        setText("summaryTitle",    "Global Pandemic Summary");
        setText("summarySubtitle", "Latest worldwide COVID-19 statistics from real-time public datasets.");

        // Hide badge + reset button
        badge?.classList.add("d-none");
        resetBtn?.classList.add("d-none");
        if (badgeName) badgeName.textContent = "—";

        setTimeout(() => setCardOpacity(1), 100);
    }

    function setText(id, value) {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    }

    function formatNum(n) {
        return Number(n).toLocaleString();
    }

    function setCardOpacity(val) {
        ["valCases", "valDeaths", "valTests", "valCountries"].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.style.opacity = val;
        });
    }
});

// =============================================================================
// 1. 7-DAY MOVING AVERAGE TREND CHART
// =============================================================================

async function loadMovingAvgChart() {
    try {
        const res = await fetch("/api/moving-average");
        if (!res.ok) throw new Error("Moving average API failed");
        const data = await res.json();

        // Sample every Nth point to avoid overcrowding (target ~300 points)
        const step = Math.max(1, Math.floor(data.dates.length / 300));
        const dates    = data.dates.filter((_, i) => i % step === 0);
        const maCases  = data.ma_cases.filter((_, i) => i % step === 0);
        const maDeaths = data.ma_deaths.filter((_, i) => i % step === 0);
        const rawCases = data.cases.filter((_, i) => i % step === 0);

        const ctx = document.getElementById("movingAvgChart").getContext("2d");

        if (movingAvgChartInstance) movingAvgChartInstance.destroy();

        movingAvgChartInstance = new Chart(ctx, {
            type: "line",
            data: {
                labels: dates,
                datasets: [
                    {
                        label: "Daily Cases (raw)",
                        data: rawCases,
                        borderColor: "rgba(59,130,246,0.2)",
                        backgroundColor: "rgba(59,130,246,0.03)",
                        borderWidth: 1,
                        pointRadius: 0,
                        fill: true,
                        tension: 0.3,
                        order: 2
                    },
                    {
                        label: "7-Day MA — Cases",
                        data: maCases,
                        borderColor: "#3b82f6",
                        backgroundColor: "transparent",
                        borderWidth: 2.5,
                        pointRadius: 0,
                        fill: false,
                        tension: 0.4,
                        order: 1
                    },
                    {
                        label: "7-Day MA — Deaths",
                        data: maDeaths,
                        borderColor: "#ef4444",
                        backgroundColor: "transparent",
                        borderWidth: 2.5,
                        pointRadius: 0,
                        fill: false,
                        tension: 0.4,
                        order: 1,
                        yAxisID: "yDeaths"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: "index", intersect: false },
                plugins: {
                    legend: { position: "bottom", labels: { usePointStyle: true, padding: 12 } },
                    tooltip: {
                        callbacks: {
                            label: ctx => `${ctx.dataset.label}: ${Number(ctx.parsed.y).toLocaleString()}`
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { maxTicksLimit: 8, maxRotation: 0 },
                        grid: { display: false }
                    },
                    y: {
                        title: { display: true, text: "Daily Cases", font: { weight: "bold" } },
                        beginAtZero: true,
                        position: "left"
                    },
                    yDeaths: {
                        title: { display: true, text: "Daily Deaths", font: { weight: "bold" } },
                        beginAtZero: true,
                        position: "right",
                        grid: { drawOnChartArea: false }
                    }
                }
            }
        });

    } catch (err) {
        console.error("Moving average chart error:", err);
    }
}

// =============================================================================
// 2. CORRELATION HEATMAP
// =============================================================================

async function loadCorrelationChart() {
    try {
        const res = await fetch("/api/correlation");
        if (!res.ok) throw new Error("Correlation API failed");
        const data = await res.json();

        const labels = data.labels;
        const matrix = data.matrix;
        const n = labels.length;

        // Build scatter-style dataset for heatmap cells
        const heatmapData = [];
        const backgroundColors = [];

        for (let row = 0; row < n; row++) {
            for (let col = 0; col < n; col++) {
                const val = matrix[row][col];
                heatmapData.push({ x: col, y: n - 1 - row, v: val });
                // Color: positive = blue, negative = red, zero = white
                const intensity = Math.abs(val);
                if (val >= 0) {
                    backgroundColors.push(`rgba(59,130,246,${0.1 + intensity * 0.85})`);
                } else {
                    backgroundColors.push(`rgba(239,68,68,${0.1 + intensity * 0.85})`);
                }
            }
        }

        const ctx = document.getElementById("correlationChart").getContext("2d");
        if (correlationChartInstance) correlationChartInstance.destroy();

        correlationChartInstance = new Chart(ctx, {
            type: "scatter",
            data: {
                datasets: [{
                    data: heatmapData,
                    backgroundColor: backgroundColors,
                    pointRadius: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: ctx => {
                                const d = ctx.raw;
                                const rowLabel = labels[n - 1 - d.y];
                                const colLabel = labels[d.x];
                                return `${rowLabel} × ${colLabel}: ${d.v.toFixed(3)}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        type: "linear", min: -0.5, max: n - 0.5,
                        ticks: { stepSize: 1, callback: v => labels[v] || "" },
                        grid: { display: false }
                    },
                    y: {
                        type: "linear", min: -0.5, max: n - 0.5,
                        ticks: { stepSize: 1, callback: v => labels[n - 1 - v] || "" },
                        grid: { display: false }
                    }
                }
            },
            plugins: [{
                id: "heatmapLabels",
                afterDatasetsDraw(chart) {
                    const ctx2 = chart.ctx;
                    const meta = chart.getDatasetMeta(0);
                    ctx2.save();
                    ctx2.font = "bold 11px sans-serif";
                    ctx2.textAlign = "center";
                    ctx2.textBaseline = "middle";

                    const cellW = chart.chartArea.width  / n;
                    const cellH = chart.chartArea.height / n;

                    heatmapData.forEach((d, i) => {
                        const xPx = chart.chartArea.left + (d.x + 0.5) * cellW;
                        const yPx = chart.chartArea.top  + (n - 1 - d.y + 0.5) * cellH;

                        // Draw cell rectangle
                        ctx2.fillStyle = backgroundColors[i];
                        ctx2.fillRect(xPx - cellW / 2 + 2, yPx - cellH / 2 + 2, cellW - 4, cellH - 4);

                        // Draw value text
                        ctx2.fillStyle = Math.abs(d.v) > 0.5 ? "#ffffff" : "#0f172a";
                        ctx2.fillText(d.v.toFixed(2), xPx, yPx);
                    });
                    ctx2.restore();
                }
            }]
        });

    } catch (err) {
        console.error("Correlation chart error:", err);
    }
}

// =============================================================================
// 3. BUBBLE CHART
// =============================================================================

async function loadBubbleChart() {
    try {
        const res = await fetch("/api/bubble");
        if (!res.ok) throw new Error("Bubble API failed");
        const data = await res.json();

        // Group by cluster
        const clusterGroups = { 0: [], 1: [], 2: [], 3: [], 4: [] };
        const maxDeaths = Math.max(...data.points.map(p => p.r), 1);

        data.points.forEach(p => {
            const scaledR = Math.max(3, Math.sqrt(p.r / maxDeaths) * 28);
            if (clusterGroups[p.cluster] !== undefined) {
                clusterGroups[p.cluster].push({
                    x: p.x,
                    y: p.y,
                    r: scaledR,
                    country: p.country,
                    date: p.date,
                    rawDeaths: p.r
                });
            }
        });

        const clusterColors = [
            { fill: "rgba(59,130,246,0.55)",  border: "#3b82f6"  },
            { fill: "rgba(16,185,129,0.55)",   border: "#10b981"  },
            { fill: "rgba(245,158,11,0.55)",   border: "#f59e0b"  },
            { fill: "rgba(239,68,68,0.55)",    border: "#ef4444"  },
            { fill: "rgba(139,92,246,0.55)",   border: "#8b5cf6"  }
        ];

        const datasets = Object.keys(clusterGroups).map(k => ({
            label: `Cluster ${k}`,
            data: clusterGroups[k],
            backgroundColor: clusterColors[k].fill,
            borderColor:     clusterColors[k].border,
            borderWidth: 1
        }));

        const ctx = document.getElementById("bubbleChart").getContext("2d");
        if (bubbleChartInstance) bubbleChartInstance.destroy();

        bubbleChartInstance = new Chart(ctx, {
            type: "bubble",
            data: { datasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom", labels: { usePointStyle: true, padding: 14 } },
                    tooltip: {
                        callbacks: {
                            label: ctx => {
                                const d = ctx.raw;
                                return [
                                    `${d.country} (${d.date})`,
                                    `Tests: ${Number(d.x).toLocaleString()}`,
                                    `Cases: ${Number(d.y).toLocaleString()}`,
                                    `Deaths: ${Number(d.rawDeaths || 0).toLocaleString()}`
                                ];
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: "Daily Tests", font: { weight: "bold" } },
                        grid: { color: "rgba(0,0,0,0.04)" }
                    },
                    y: {
                        title: { display: true, text: "Daily Cases", font: { weight: "bold" } },
                        beginAtZero: true
                    }
                }
            }
        });

    } catch (err) {
        console.error("Bubble chart error:", err);
    }
}