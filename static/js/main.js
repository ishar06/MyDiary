// Automatically set today's date in the title field when creating a new entry
document.addEventListener('DOMContentLoaded', function() {
    const titleInput = document.querySelector('#title');
    if (titleInput && !titleInput.value) {
        const today = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        titleInput.value = today.toLocaleDateString(undefined, options);
    }

    // Handle flash message dismissal
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }, 3000);
    });

    // Enable Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});