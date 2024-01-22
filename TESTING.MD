
# Testing Documentation

This document outlines the testing strategies and results for the Spark Dating App, ensuring functionality, usability, and accessibility across various aspects of the application.

## Automated Testing

### Django Tests

**Models:**
- Each Django model was tested to ensure proper field initialization, data types, relationships, and method outputs.

**Views:**
- View tests checked the correct templates were rendered, context variables were passed, and redirects occurred as expected.

**Forms:**
- Form tests validated field requirements, default values, and error handling.

## Manual Testing

### Browser Compatibility
Tested on multiple browsers (Chrome, Firefox, Safari, and Edge) to ensure cross-browser compatibility.

### Mobile Responsiveness
Verified the site’s responsiveness and functionality on various devices (phones, tablets, laptops).

### User Stories Testing

**First-Time Visitor Goals:**
- Checked site navigation and sign-up process.
- Verified the ease of understanding site functionalities.

**Returning Visitor Goals:**
- Tested for new message notifications and swiping functionality.
- Checked for updates and enhancements in user experience.

**Frequent Visitor Goals:**
- Focused on chat functionality and match interactions.

### Functionality Testing

- **Navigation Links:** Ensured all navigation links lead to the correct pages.
- **User Authentication:** Tested the sign-up, login, and logout processes.
- **Profile Management:** Validated the creation, editing, and deletion of user profiles.
- **Matchmaking:** Tested the swipe mechanism and match generation.
- **Chat System:** Checked real-time messaging, message retrieval, and UI updates.

### Accessibility Testing

- Ran the website through tools like [WAVE](https://wave.webaim.org/) to identify and fix accessibility issues.
- Manually checked color contrasts and screen reader compatibility.

## Validation

- **HTML:** Used the [W3C HTML Validator](https://validator.w3.org/) to validate HTML files.
- **CSS:** Utilized [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) for CSS validation.
- **JavaScript:** Checked code quality and errors using [JSHint](https://jshint.com/).

## Known Bugs

- When you send a message sometimes it will fetch it right away but when the page 
 reloads there are now two of the message you just sent 

## Conclusion

The testing process has been thorough, ensuring that the Spark Dating App offers a reliable, user-friendly, and accessible platform for its audience. Continuous monitoring will be in place for addressing any future issues and enhancing user experience.
