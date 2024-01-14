document.addEventListener('DOMContentLoaded', function() {
    const profileLinks = document.querySelectorAll('.profile-link');

    profileLinks.forEach(link => {
        let clickedOnce = false;
        let timeout;

        const hideOverlay = (overlay) => {
            overlay.style.display = 'none';
            clickedOnce = false;
        };

        link.addEventListener('click', function(event) {
            const overlayMessage = this.querySelector('.overlay-message');
            if (!clickedOnce) {
                event.preventDefault(); // Prevent link navigation
                // Show the overlay message
                overlayMessage.style.display = 'block';
                clickedOnce = true;

                // Set a timeout to hide the message after 3 seconds (3000 milliseconds)
                clearTimeout(timeout); // Clear any existing timeout
                timeout = setTimeout(() => hideOverlay(overlayMessage), 3000);
            } else {
                // On second click, hide the message immediately
                hideOverlay(overlayMessage);
            }
        });
    });
});
