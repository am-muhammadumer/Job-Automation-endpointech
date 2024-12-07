// Define the toggleForm function
function toggleForm() {
    const formContainer = document.getElementById("add-dice-profile");
    formContainer.classList.toggle("show");
}
function closeForm() {
    document.getElementById('add-dice-profile').classList.remove('show');
}

document.getElementById("toggleButton").addEventListener("click", function () {
    const playIcon = document.getElementById("play");
    const pauseIcon = document.getElementById("pause");

    if (playIcon.style.display === "none") {
        playIcon.style.display = "inline";
        pauseIcon.style.display = "none";
    } else {
        playIcon.style.display = "none";
        pauseIcon.style.display = "inline";
    }
});


document.querySelectorAll('.toggleButton').forEach(button => {
    button.addEventListener('click', async function(event) {
        event.preventDefault(); // Prevent default anchor behavior

        const diceId = button.getAttribute('dice-id');
        
        // Find play/pause icons within the clicked button's scope
        const playIcon = button.querySelector('.play-icon');
        const pauseIcon = button.querySelector('.pause-icon');
        const isPlay = playIcon.style.display !== 'none'; // Check current state

        try {
            // Send the API request to toggle dice status
            const response = await fetch(`/change_dice_status/${diceId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ new_status: isPlay ? 'running' : 'stopped' })
            });

            const data = await response.json();

            if (data.success) {
                // Toggle button icons
                playIcon.style.display = isPlay ? 'none' : 'inline';
                pauseIcon.style.display = isPlay ? 'inline' : 'none';
            } else {
                console.error('Server Error:', data.message || 'Failed to toggle dice status');
                alert('Error: ' + (data.message || 'An unexpected error occurred.'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while toggling the dice status. Please try again.');
        }
    });
});
