document.getElementById("search").addEventListener("keyup", function() {
    let filter = this.value.toLowerCase();
    let rows = document.querySelectorAll("tbody tr");

    rows.forEach(row => {
        let text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? "" : "none";
    });
});


// Fetch and display top 10 employees
fetch('/top_employees')
    .then(response => response.json())
    .then(data => {
        let table = document.querySelector("tbody");
        table.innerHTML = "";  // Clear table

        data.forEach(emp => {
            let row = `<tr>
                <td>${emp._id}</td>
                <td>${emp.total_hours}</td>
            </tr>`;
            table.innerHTML += row;
        });
    });

document.addEventListener("DOMContentLoaded", function () {
    fetch('/work_hours')
        .then(response => response.json())
        .then(data => {
            let labels = [];
            let values = [];
   
            data.forEach(item => {
                labels.push(`${item.employee_id} (${item.date})`);
                values.push(item.work_hours);
            });
   
            updateWorkHoursChart(labels, values);
        })
        .catch(error => console.error('Error fetching work hours:', error));
});
    
function updateWorkHoursChart(labels, values) {
    var ctx = document.getElementById('workHoursChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Work Hours',
                data: values,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
    