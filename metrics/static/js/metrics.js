const url = "api/";
const plotlyOptions = { responsive: true };
const legendConfig = {
    showlegend: true,
    legend: { orientation: "h", x: 0.1, y: 1.15 }
};
const plotlyLayout = {
    margin: { l: 40, r: 20, t: 30, b: 40 },
    autosize: true,
    automargin: true,
    height: 400,
};
const greenColor = "rgb(17, 140, 79)";
const greyColor = "rgb(184, 184, 184)";
const redColor = "rgb(255, 50, 23)";

function loadMetrics(year) {
    const prevYear = year - 1;

    function setTrend(elementId, current, previous, inverted = false) {
        const el = document.getElementById(elementId);
        if (!el || previous === 0) {
            el.innerText = '—';
            return;
        }
        const trend = Math.round(((current - previous) / previous) * 100);
        const icon = trend > 0 ? '↑' : trend < 0 ? '↓' : '→';
        
        // Inverted = lower is better (cancellations, maintenance costs)
        let cls;
        if (trend === 0) {
            cls = 'text-muted';
        } else if (inverted) {
            cls = trend > 0 ? 'text-danger' : 'text-success';
        } else {
            cls = trend > 0 ? 'text-success' : 'text-danger';
        }
        
        el.innerHTML = `<span class="${cls}">${icon} ${Math.abs(trend)}% vs ${year - 1}</span>`;
    }

    // In Promise.all for summary stats
    Promise.all([
        fetch(url + `?reservations=true&year=${year}`).then(r => r.json()),
        fetch(url + `?reservations=true&year=${year - 1}`).then(r => r.json()),
        fetch(url + `?cancellations=true&year=${year}`).then(r => r.json()),
        fetch(url + `?cancellations=true&year=${year - 1}`).then(r => r.json()),
        fetch(url + `?cancellation_rate=true&year=${year}`).then(r => r.json()),
        fetch(url + `?maintenance_costs=true&year=${year}`).then(r => r.json()),
        fetch(url + `?maintenance_costs=true&year=${year - 1}`).then(r => r.json()),
    ]).then(([
        currentRes, previousRes,
        currentCanc, previousCanc,
        cancRate,
        currentMaint, previousMaint
    ]) => {
        // Totals
        const totalRes = currentRes.reduce((sum, r) => sum + r.total, 0);
        const totalPrevRes = previousRes.reduce((sum, r) => sum + r.total, 0);
        const totalCanc = currentCanc.reduce((sum, r) => sum + r.total, 0);
        const totalPrevCanc = previousCanc.reduce((sum, r) => sum + r.total, 0);

        // Update stats
        document.getElementById('stat-reservations').innerText = totalRes;
        document.getElementById('stat-cancellations').innerText = totalCanc;
        document.getElementById('stat-cancellation-rate').innerText = `${cancRate.rate}%`;
        const cost = currentMaint.cost__sum || 0;
        document.getElementById('stat-maintenance').innerText = `$${parseFloat(cost).toFixed(2)}`;

        // Update trends
        setTrend('trend-reservations', totalRes, totalPrevRes);
        setTrend('trend-cancellations', totalCanc, totalPrevCanc, true);
        setTrend('trend-maintenance', 
            currentMaint.cost__sum || 0, 
            previousMaint.cost__sum || 0,
            true
        );

        // Cancellation rate trend
        const rateEl = document.getElementById('trend-cancellation-rate');
        rateEl.innerText = cancRate.rate === 0 ? '✓ No cancellations' : '';

    }).catch(err => console.error('Summary stats error:', err));

    // Chart 1 — Reservations per Month (year over year)
    Promise.all([
        fetch(url + `?reservations=true&year=${year}`).then(r => r.json()),
        fetch(url + `?reservations=true&year=${prevYear}`).then(r => r.json()),
    ]).then(([currentYear, lastYear]) => {
        const months = currentYear.map(r => r.month);
        Plotly.newPlot('chart-1', [
            {
                x: months,
                y: currentYear.map(r => r.total),
                mode: 'lines',
                name: `${year}`,
                line: { color: greenColor }
            },
            {
                x: months,
                y: lastYear.map(r => r.total),
                mode: 'lines',
                name: `${prevYear}`,
                line: { dash: "dashdot", color: greyColor }
            }
        ], {
            ...legendConfig,
            ...plotlyLayout,
            xaxis: { title: 'Month' },
            yaxis: { title: 'Reservations' }
        }, plotlyOptions);
    }).catch(err => console.error('Chart 1 error:', err));

    // Chart 2 — Cancellations per Month
    fetch(url + `?cancellations=true&year=${year}`)
        .then(r => r.json())
        .then(data => {
            Plotly.newPlot('chart-2', [{
                x: data.map(r => r.month),
                y: data.map(r => r.total),
                type: 'bar',
                name: `${year}`,
                marker: { color: redColor }
            }], {
                ...legendConfig,
                ...plotlyLayout,
                xaxis: { title: 'Month' },
                yaxis: { title: 'Cancellations', rangemode: 'nonnegative'}
            }, plotlyOptions);
        }).catch(err => console.error('Chart 2 error:', err));

    // Chart 3 — Maintenance Costs (year over year)
    Promise.all([
        fetch(url + `?maintenance_costs=true&year=${year}`).then(r => r.json()),
        fetch(url + `?maintenance_costs=true&year=${prevYear}`).then(r => r.json()),
    ]).then(([currentCosts, lastCosts]) => {
        Plotly.newPlot('chart-3', [{
            x: [String(prevYear), String(year)],
            y: [lastCosts.cost__sum || 0, currentCosts.cost__sum || 0],
            type: 'bar',
            marker: { color: [greyColor, greenColor] }
        }], {
            ...plotlyLayout,
            xaxis: { type: "category", title: "Year" },
            yaxis: { title: "Costs ($)" }
        }, plotlyOptions);
    }).catch(err => console.error('Chart 3 error:', err));

    // Chart 4 — Most Popular Sites (not year dependent)
    fetch(url + `?popular_sites=true`)
        .then(r => r.json())
        .then(data => {
            Plotly.newPlot('chart-4', [{
                x: data.map(r => `Site ${r.site}`),
                y: data.map(r => r.total),
                type: 'bar',
                marker: { color: greenColor }
            }], {
                ...plotlyLayout,
                xaxis: { title: 'Site' },
                yaxis: { title: 'Total Reservations' }
            }, plotlyOptions);
        }).catch(err => console.error('Chart 4 error:', err));

        // Chart 5 — Long Term vs Short Term
        fetch(url + `?reservation_types=true`)
            .then(r => r.json())
            .then(data => {
                Plotly.newPlot('chart-5', [{
                    values: [data.long_term, data.short_term],
                    labels: ['Long Term', 'Short Term'],
                    type: 'pie',
                    hole: 0.4,  // donut style
                    marker: {
                        colors: [greenColor, greyColor]
                    },
                    textinfo: 'label+percent',
                    hoverinfo: 'label+value+percent'
                }], {
                    ...plotlyLayout,
                    showlegend: true,
                    legend: { orientation: "h", x: 0.2, y: -0.1 },
                    annotations: [{
                        text: `${data.total}<br>Total`,
                        x: 0.5,
                        y: 0.5,
                        font: { size: 14 },
                        showarrow: false
                    }]
                }, plotlyOptions);
            }).catch(err => console.error('Chart 5 error:', err));
}

// Initial load
let currentYear = new Date().getFullYear();
loadMetrics(currentYear);

// Year selector
document.getElementById('year-select').addEventListener('change', function() {
    currentYear = parseInt(this.value);
    loadMetrics(currentYear);
});