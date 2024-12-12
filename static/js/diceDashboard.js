// Define the toggleForm function
function toggleForm() {
    const formContainer = document.getElementById("add-dice-profile");
    formContainer.classList.toggle("show");
}
function closeForm() {
    document.getElementById('add-dice-profile').classList.remove('show');
}

document.querySelectorAll('.toggleButton').forEach(button => {
    button.addEventListener('click', async function (event) {
        event.preventDefault(); // Default behavior ko rokiye

        const diceId = button.getAttribute('dice-id');
        const playIcon = button.querySelector('.fa-play'); // Play icon select karen
        const pauseIcon = button.querySelector('.fa-pause'); // Pause icon select karen
        const isPlay = playIcon.style.display !== 'none'; // Check karein ki play icon visible hai ya nahi

        try {
            // Backend ko request bhejiye
            const response = await fetch(`/change_dice_status/${diceId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ new_status: isPlay ? 'running' : 'stopped' }),
            });

            const data = await response.json();

            if (data.success) {
                // Icons ko toggle karein
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
