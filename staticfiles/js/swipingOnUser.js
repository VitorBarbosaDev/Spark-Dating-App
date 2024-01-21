document.querySelectorAll('.btn-yes, .btn-no').forEach(button => {
    button.addEventListener('click', event => {
        event.preventDefault();
        let swipedOnUsername = button.dataset.username;
        let like = button.classList.contains('btn-yes');

        let method = like ? 'POST' : 'POST';
        let endpoint = like ? `/like/${swipedOnUsername}/` : `/dislike/${swipedOnUsername}/`;

        // Save a reference to the current profile card
        let currentProfileCard = event.currentTarget.closest('.profile-card');

        fetch(endpoint, {
            method: method,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.match) {
                    // Set match message
                    var matchModal = new bootstrap.Modal(document.getElementById('matchModal'));

                    matchModal.show();
                }

                if (data.next_profile) {
                    // Remove current profile card if it still exists
                    if (currentProfileCard && document.body.contains(currentProfileCard)) {
                        currentProfileCard.remove();
                    }

                    let newProfileCard = createProfileCard(data.next_profile);
                    let rowContainer = document.querySelector('.profile-container-outer .row.d-flex.justify-content-center.align-items-center');
                    if (rowContainer) {
                        rowContainer.appendChild(newProfileCard);
                    }
                } else {
                    displayNoProfilesMessage();

                    // Remove the last profile card if it still exists
                    if (currentProfileCard && document.body.contains(currentProfileCard)) {
                        currentProfileCard.remove();
                    }
                }
            })
            .catch(error => console.error('Error:', error));
    });
});




function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function createProfileCard(profileData) {


    // Extracting the necessary data from profileData
    const { username, first_name, age, bio, genderIcon, id, profile_url, images, interests } = profileData;

    // Function to truncate bio
    function truncateBio(bio, maxWords) {
        let words = bio.split(' ');
        if (words.length > maxWords) {
            return words.slice(0, maxWords).join(' ') + '...';
        }
        return bio;
    }

    // Truncate bio to 20 words
    let truncatedBio = truncateBio(bio, 20);
    let interestElements = interests.map(interest => `<i class="${interest.icon}"></i> ${interest.name}`).join(', ');


    let card = document.createElement('div');
    card.className = 'col-md-6 col-lg-4 mb-4 profile-card';

    let carouselItems = '';
    if (Array.isArray(images) && images.length) {
        carouselItems = images.map((image, index) => {
            return `
                <div class="carousel-item ${index === 0 ? 'active' : ''}">
                    <img src="${image}" class="d-block w-100 rounded-image-top" alt="${username}">
                </div>
            `;
        }).join('');
    } else {
        // Fallback content if no images are available
        carouselItems = `<div class="carousel-item active">
                             <img src="/path/to/default/image.png" class="d-block w-100 rounded-image-top" alt="Default Image">
                         </div>`;
    }

    // Constructing the card's inner HTML
    card.innerHTML = `
        <a href="${profile_url}" class="profile-link">
            <div class="card">
                <div id="carousel${id}" class="carousel slide main-bg carousel-border" data-bs-ride="carousel">
                    <div class="carousel-inner rounded-image-top">
                        ${carouselItems}
                    </div>
                    <div class="tap-message">Tap To See More On ${first_name}</div>
                    <div class="overlay-message">Click again to see more</div>
                    <a class="carousel-control-prev" href="#carousel${id}" role="button" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="sr-only">Previous</span>
                    </a>
                    <a class="carousel-control-next" href="#carousel${id}" role="button" data-bs-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="sr-only">Next</span>
                    </a>
                </div>
                <div class="card-body">
                    <h2 class="card-title">${username}</h2>
                    <p class="card-text text-muted h6">${first_name}, ${age} years old, <i class="${genderIcon}"></i> ${profileData.gender}</p>
                    <p class="card-text">Interests: ${interestElements}</p>
                    <p class="card-text">${truncatedBio}</p>
                    <div class="text-center">
                        <a href="#" class="btn btn-yes btn-sm" data-username="${username}">Yes</a>
                        <a href="#" class="btn btn-no btn-sm" data-username="${username}">No</a>
                    </div>
                </div>
            </div>
        </a>
    `;

    // Attach event listeners to the new buttons
    attachSwipeEventListeners(card, username);

    return card;
}



function attachSwipeEventListeners(card, username) {
    const yesButton = card.querySelector('.btn-yes');
    const noButton = card.querySelector('.btn-no');
    if (yesButton && noButton) {
        yesButton.setAttribute('data-username', username);
        noButton.setAttribute('data-username', username);
        yesButton.addEventListener('click', event => swipeAction(event, username, true));
        noButton.addEventListener('click', event => swipeAction(event, username, false));
    }
}

function swipeAction(event, username, like) {
    event.preventDefault();

    let method = 'POST';
    let endpoint = like ? `/like/${username}/` : `/dislike/${username}/`;

    fetch(endpoint, {
        method: method,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.match) {
                // Set match message
                var matchModal = new bootstrap.Modal(document.getElementById('matchModal'));

                matchModal.show();
            }

            // Check if the element that triggered the event is still in the DOM
            let buttonElement = document.querySelector(`[data-username="${username}"]`);
            let currentProfileCard = buttonElement ? buttonElement.closest('.profile-card') : null;

            if (data.next_profile) {
                // Remove current profile card if it exists
                if (currentProfileCard) {
                    currentProfileCard.remove();
                }

                // Create and add a new profile card
                let newProfileCard = createProfileCard(data.next_profile);
                let rowContainer = document.querySelector('.profile-container-outer .row.d-flex.justify-content-center.align-items-center');
                if (rowContainer) {
                    rowContainer.appendChild(newProfileCard);
                }
            } else {
                // Display 'No more profiles' message and remove the last profile card
                displayNoProfilesMessage();
                if (currentProfileCard) {
                    currentProfileCard.remove();
                }
            }
        })
        .catch(error => console.error('Error:', error));
}

function displayNoProfilesMessage() {
    let container = document.querySelector('.profile-container-outer');
    if (container) {
        container.innerHTML = '<div class="container">\n' +
            '            <div class="row justify-content-center">\n' +
            '                <div class="col-md-6 col-lg-4">\n' +
            '                    <div class="card">\n' +
            '                        <div class="card-body">\n' +
            '                            <h1 class="text-center mb-4">No More Profiles Found</h1>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </div>\n' +
            '            </div>\n' +
            '        </div>';
    }
}

function swipeActionProfilePage(event, username, like) {
    event.preventDefault();

    let method = 'POST';
    let endpoint = like ? `/like/${username}/` : `/dislike/${username}/`;

    fetch(endpoint, {
        method: method,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.match) {
                // Set match message
                document.getElementById('matchMessage').textContent = data.message;

                // Show the modal
                var matchModal = new bootstrap.Modal(document.getElementById('matchModal'));
                matchModal.show();

                // Add event listener to redirect to home page after closing the modal
                document.getElementById('matchModal').addEventListener('hidden.bs.modal', () => {
                    window.location.href = '/'; // Redirect to home page
                });
            } else {
                // No match, redirect to home page
                window.location.href = '/';
            }
        })
        .catch(error => console.error('Error:', error));
}

// Attach event listeners to Yes and No buttons
document.querySelectorAll('.btn-yes, .btn-no').forEach(originalButton => {
    // Clone the button and replace the original with the clone
    let clonedButton = originalButton.cloneNode(true);
    originalButton.parentNode.replaceChild(clonedButton, originalButton);

    // Now attach the event listener to the cloned button
    clonedButton.addEventListener('click', event => {
        event.preventDefault();
        let username = clonedButton.getAttribute('data-username');
        let like = clonedButton.classList.contains('btn-yes');
        swipeActionProfilePage(event, username, like);
    });
});


