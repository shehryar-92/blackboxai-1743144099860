document.addEventListener('DOMContentLoaded', () => {
    // Initialize WebSocket connection
    const socket = new WebSocket(`ws://${window.location.host}/ws`);

    // Chart initialization
    const ctx = document.getElementById('earnings-chart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Earnings ($)',
                data: [],
                borderColor: 'rgb(79, 70, 229)',
                tension: 0.1,
                fill: true,
                backgroundColor: 'rgba(79, 70, 229, 0.1)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Handle incoming data
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        updateDashboard(data);
    };

    // Update dashboard elements
    function updateDashboard(data) {
        // Update balance and payment info
        document.getElementById('current-balance').textContent = `$${data.current_balance.toFixed(2)}`;
        document.getElementById('last-payment').textContent = `$${data.last_payment.amount.toFixed(2)}`;
        document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
        
        // Update transactions table
        const tableBody = document.getElementById('transactions-table');
        tableBody.innerHTML = data.recent_transactions.map(tx => `
            <tr>
                <td class="px-6 py-4 whitespace-nowrap">${new Date(tx.timestamp).toLocaleString()}</td>
                <td class="px-6 py-4 whitespace-nowrap">$${tx.amount.toFixed(2)}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 py-1 text-xs rounded-full ${tx.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                        ${tx.status}
                    </span>
                </td>
            </tr>
        `).join('');
        
        // Update chart data
        chart.data.labels = data.history.map(item => new Date(item.date).toLocaleDateString());
        chart.data.datasets[0].data = data.history.map(item => item.amount);
        chart.update();
        
        // Handle anomalies
        const anomalyElement = document.getElementById('anomaly-status');
        if (data.anomaly_detected) {
            anomalyElement.className = 'p-3 bg-red-100 text-red-800 rounded blink-warning';
            anomalyElement.textContent = '⚠ Anomaly detected in recent transactions';
        } else {
            anomalyElement.className = 'p-3 bg-green-100 text-green-800 rounded';
            anomalyElement.textContent = 'No anomalies detected';
        }
    }

    // Handle connection status
    socket.onclose = () => {
        document.getElementById('connection-status').className = 'px-3 py-1 bg-red-500 rounded-full text-sm';
        document.getElementById('connection-status').textContent = 'Disconnected';
    };
});