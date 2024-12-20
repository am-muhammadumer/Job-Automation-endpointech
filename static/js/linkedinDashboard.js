// Toggle visibility of the form
function toggleForm() {
    const formContainer = document.getElementById('add-linkedin-profile');
    formContainer.classList.toggle('show');
}

// Close the form
function closeForm() {
    const formContainer = document.getElementById('add-linkedin-profile');
    formContainer.classList.remove('show');
}


document.querySelectorAll('.toggleButton').forEach(button => {
    button.addEventListener('click', async function (event) {
        event.preventDefault(); // Prevent default behavior

        const linkedinId = button.getAttribute('linkedin-id'); // Get the LinkedIn ID
        const playIcon = button.querySelector('.fa-play'); // Select Play icon
        const pauseIcon = button.querySelector('.fa-pause'); // Select Pause icon
        const isPlay = playIcon.style.display !== 'none'; // Check if Play icon is visible

        try {
            // Send a request to the backend
            const response = await fetch(`/change_bot_status/linkedin/${linkedinId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ new_status: isPlay ? 'running' : 'stopped' }),
            });

            const data = await response.json();

            if (data.success) {
                // Toggle the icons
                playIcon.style.display = isPlay ? 'none' : 'inline';
                pauseIcon.style.display = isPlay ? 'inline' : 'none';
            } else {
                console.error('Server Error:', data.message || 'Failed to toggle LinkedIn bot status');
                alert('Error: ' + (data.message || 'An unexpected error occurred.'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while toggling the LinkedIn bot status. Please try again.');
        }
    });
});


// document.querySelectorAll('.toggleButton').forEach((button) => {
//     button.addEventListener('click', (event) => {
//         event.preventDefault();  // Prevent default anchor behavior
        
//         const linkedinId = button.getAttribute('linkedin-id'); // Get LinkedIn ID
//         const playIcon = button.querySelector('.play-icon'); // Play icon
//         const pauseIcon = button.querySelector('.pause-icon'); // Pause icon

//         // Check if the status is running or stopped based on the current visibility of the icons
//         const isRunning = playIcon.classList.contains('hidden');
//         playIcon.classList.toggle('hidden', !isRunning);
//         pauseIcon.classList.toggle('hidden', isRunning);

//         // Set the new status based on the current state
//         const newStatus = isRunning ? 'stopped' : 'running';  // Toggle status between running and stopped

//         // Send the new status to the backend
//         updateBotStatus(linkedinId, newStatus);
//     });
// });


// // Update bot status in the backend
// function updateBotStatus(linkedinId, status) {
//     fetch(`/change_bot_status/linkedin/${linkedinId}`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ linkedin_id: linkedinId, status: status })
//     })
//         .then((response) => response.json())
//         .then((data) => {
//             if (!data.success) {
//                 console.error('Failed to update status:', data.message);
//                 alert(`Error updating status: ${data.message}`);
//             } else {
//                 console.log('Status updated:', data.message);
//             }
//         })
//         .catch((error) => {
//             console.error('Error:', error);
//             alert('An error occurred while updating the bot status.');
//         });
// }
