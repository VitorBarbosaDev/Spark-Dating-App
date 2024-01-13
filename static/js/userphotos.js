document.addEventListener('DOMContentLoaded', function () {
    const profileContainers = document.querySelectorAll('.profile-container');

    profileContainers.forEach(container => {
        let currentImageIndex = 0;
        const images = container.querySelectorAll('.image-container img'); // Targeting img tags
        const nextButton = container.querySelector('.next-button');
        const prevButton = container.querySelector('.prev-button');

        if (images.length > 0) {
            images[0].style.display = 'block'; // Show the first image initially

            nextButton.addEventListener('click', function () {
                images[currentImageIndex].style.display = 'none';
                currentImageIndex = (currentImageIndex + 1) % images.length;
                images[currentImageIndex].style.display = 'block';
            });

            prevButton.addEventListener('click', function () {
                images[currentImageIndex].style.display = 'none';
                currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
                images[currentImageIndex].style.display = 'block';
            });
        }
    });
});
