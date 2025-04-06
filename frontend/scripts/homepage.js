document.addEventListener('DOMContentLoaded', function () {
    // Buttons
    const reserveBtn = document.getElementById('reserve-btn');
    const availabilityBtn = document.getElementById('availability-btn');

    reserveBtn.addEventListener('click', function () {
        window.open('https://lib.usf.edu/services/reserving-library-spaces/', '_blank');
    });

    availabilityBtn.addEventListener('click', function () {
        window.location.href = 'availabilitymap.html';
    });

    // Toggle logout popup
    const profileIcon = document.getElementById('profile-icon');
    const logoutPopup = document.getElementById('logout-popup');

    profileIcon.addEventListener('click', () => {
        logoutPopup.style.display = logoutPopup.style.display === 'block' ? 'none' : 'block';
    });

    // Hide popup when clicking outside
    window.addEventListener('click', function (e) {
        if (!document.querySelector('.profile-container').contains(e.target)) {
            logoutPopup.style.display = 'none';
        }
    });
});
