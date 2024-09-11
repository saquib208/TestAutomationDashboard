$(document).ready(function() {
    // Debugging: Log the reportData to the console
    console.log('Report Data:', reportData);

    // Prepare data for the Chart.js pie chart
    const passed = reportData.total_tests - reportData.failures - reportData.errors - reportData.skipped;
    const failed = reportData.failures + reportData.errors;
    const skipped = reportData.skipped;

    var ctx = document.getElementById('testResultsChart').getContext('2d');
    var testResultsChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Passed', 'Failed', 'Skipped'],
            datasets: [{
                data: [passed, failed, skipped],
                backgroundColor: ['#28a745', '#dc3545', '#ffc107'],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Test Results Overview'
                }
            }
        },
    });

    // Filter test cases based on status
    $('#statusFilter').on('change', function() {
        var selectedStatus = $(this).val();
        filterTestCases(selectedStatus, $('#searchBox').val().trim().toLowerCase());
    });

    // Search test cases based on Test Case ID, Service Name, or Name
    $('#searchBox').on('input', function() {
        var query = $(this).val().trim().toLowerCase();
        filterTestCases($('#statusFilter').val(), query);
    });

    // Function to filter test cases based on status and search query
    function filterTestCases(status, query) {
        $('.accordion-item').each(function() {
            var itemStatus = $(this).data('status');
            var itemName = $(this).data('name').toLowerCase();
            var itemId = $(this).data('id').toLowerCase();
            var serviceName = itemName.split('.')[0].slice(4).toLowerCase(); // Extract service name (assuming it's prefixed)

            // Check if the item matches both the status and the search query
            var statusMatch = (status === 'all') || (itemStatus === status);
            var queryMatch = (query === '') || (itemName.includes(query) || itemId.includes(query) || serviceName.includes(query));

            // Show or hide the test case based on the filters
            if (statusMatch && queryMatch) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }
});
