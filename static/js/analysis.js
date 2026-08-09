document.addEventListener("DOMContentLoaded", function() {

    // Common Chart.js options for beautiful styling
    Chart.defaults.font.family = "'Poppins', sans-serif";
    Chart.defaults.color = "#64748b";
    
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: 'rgba(15, 23, 42, 0.9)',
                titleFont: { size: 14, weight: 'bold' },
                bodyFont: { size: 13 },
                padding: 12,
                cornerRadius: 8,
                displayColors: true
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(226, 232, 240, 0.6)',
                    drawBorder: false,
                },
                ticks: {
                    maxTicksLimit: 6,
                    callback: function(value) {
                        if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M';
                        if (value >= 1000) return (value / 1000).toFixed(1) + 'K';
                        return value;
                    }
                }
            },
            x: {
                grid: {
                    display: false,
                    drawBorder: false,
                },
                ticks: {
                    maxTicksLimit: 12
                }
            }
        }
    };

    // 1. Global Cases Trend (Line Chart)
    fetch('/api/moving-average')
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById('casesTrendChart').getContext('2d');
            
            // Gradient fill
            let gradient = ctx.createLinearGradient(0, 0, 0, 400);
            gradient.addColorStop(0, 'rgba(59, 130, 246, 0.5)');
            gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: '7-Day Moving Avg Cases',
                        data: data.ma_cases,
                        borderColor: '#3b82f6',
                        backgroundColor: gradient,
                        borderWidth: 2,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: commonOptions
            });
        });

    // 2. Global Deaths Trend (Line Chart)
    fetch('/api/moving-average')
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById('deathsTrendChart').getContext('2d');
            
            let gradient = ctx.createLinearGradient(0, 0, 0, 400);
            gradient.addColorStop(0, 'rgba(239, 68, 68, 0.5)');
            gradient.addColorStop(1, 'rgba(239, 68, 68, 0.0)');

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: '7-Day Moving Avg Deaths',
                        data: data.ma_deaths,
                        borderColor: '#ef4444',
                        backgroundColor: gradient,
                        borderWidth: 2,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: commonOptions
            });
        });

    // 3. COVID Hotspots (Doughnut/Bar Chart)
    fetch('/api/top-hotspots')
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById('hotspotsChart').getContext('2d');
            
            const hotspotOptions = JSON.parse(JSON.stringify(commonOptions));
            hotspotOptions.scales.x.display = false;
            hotspotOptions.scales.y.display = false;
            hotspotOptions.plugins.legend.display = true;
            hotspotOptions.plugins.legend.position = 'right';

            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.countries,
                    datasets: [{
                        data: data.cases,
                        backgroundColor: [
                            '#065f46', '#059669', '#10b981', '#34d399', '#6ee7b7',
                            '#047857', '#0f766e', '#14b8a6', '#2dd4bf', '#5eead4'
                        ],
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }]
                },
                options: hotspotOptions
            });
        });

    // 4. Global Testing Trend (Line/Area Chart)
    fetch('/api/global-trend')
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById('testsTrendChart').getContext('2d');
            
            let gradient = ctx.createLinearGradient(0, 0, 0, 400);
            gradient.addColorStop(0, 'rgba(245, 158, 11, 0.5)');
            gradient.addColorStop(1, 'rgba(245, 158, 11, 0.0)');

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: 'Daily Tests',
                        data: data.tests,
                        borderColor: '#f59e0b',
                        backgroundColor: gradient,
                        borderWidth: 2,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                        fill: true,
                        tension: 0.2
                    }]
                },
                options: commonOptions
            });
        });

    // 5. Top Countries by Cases (Horizontal Bar Chart)
    fetch('/api/analysis/top-countries')
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById('topCountriesChart').getContext('2d');
            
            const barOptions = JSON.parse(JSON.stringify(commonOptions));
            barOptions.indexAxis = 'y'; // horizontal bar chart
            barOptions.scales.x.display = true;
            barOptions.scales.x.grid.display = true;
            barOptions.scales.y.grid.display = false;

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Total Cases',
                        data: data.data,
                        backgroundColor: '#8b5cf6',
                        borderRadius: 6
                    }]
                },
                options: barOptions
            });
        });

    // 6. Mortality Rate Analysis (Bar Chart)
    fetch('/api/analysis/mortality')
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById('mortalityChart').getContext('2d');
            
            const mortalityOptions = JSON.parse(JSON.stringify(commonOptions));
            mortalityOptions.scales.y.ticks.callback = function(value) { return value + '%'; };

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Case Fatality Rate (%)',
                        data: data.data,
                        backgroundColor: '#ec4899',
                        borderRadius: 6
                    }]
                },
                options: mortalityOptions
            });
        });

});
