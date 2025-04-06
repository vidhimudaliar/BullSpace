let failedAttempts = 0; // failed login attempts
const maxAttempts = 3; 
const blockDuration = 60000; // milliseconds (1 minute)
let isLockedOut = false; // track if the user is locked out

document.getElementById('loginForm').addEventListener('submit', function (event) {
    // Prevent the default form submission
    event.preventDefault();

    // Check if user is currently locked out:
    if (isLockedOut) {
        return; // exit if locked out
    }

    // Get the username and password values:
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Check credentials:
    if (username === 'student@usf.edu' && password === 'password123') {
        // Redirect to homepage.html if credentials are correct
        window.location.href = 'homepage.html';
    } 
    else 
    { 
        failedAttempts++; // Increment the failed attempts counter

/*---------------------Error Message------------------------------*/

        // Error message if credentials are incorrect:
        const errorMessage = document.getElementById('error-message');

        // Only show error message if attempts are below maximum:
        if (failedAttempts < maxAttempts) {
            errorMessage.textContent = 'Invalid username or password.';
            errorMessage.style.display = 'block'; 

            // Hide the error message after 1.5 seconds(1500 ms)
            setTimeout(() => {
                errorMessage.style.display = 'none'; // hide message
            }, 1500); 
        } else {
            // Hide error message after lockout occurs:
            errorMessage.style.display = 'none'; 
        }

/*----------------------Lockout Time-----------------------------*/

        // Check if maximum attempts reached
        if (failedAttempts >= maxAttempts) {
            // Disable the form inputs and button
            document.getElementById('username').disabled = true;
            document.getElementById('password').disabled = true;
            document.querySelector('button[type="submit"]').disabled = true;

            // Persistent lockout-message
            const blockMessage = document.getElementById('lockout-message');
            blockMessage.textContent =
                'Too many failed attempts. Your account has been locked for 1 minute, please try again later.';
            blockMessage.style.display = 'block'; // make it visible

            isLockedOut = true; // set lockout flag

            // Re-enable the form after 1 minute (lockout period ends)
            setTimeout(() => {
                failedAttempts = 0; // Reset failed attempts counter
                isLockedOut = false; // Reset lockout flag

                document.getElementById('username').disabled = false;
                document.getElementById('password').disabled = false;
                document.querySelector('button[type="submit"]').disabled = false;

                blockMessage.style.display = 'none'; // hide block message 
                blockMessage.textContent = ''; // clear message text

            }, blockDuration);

/*-------------------------------------------------------------*/
        }
    }
});

