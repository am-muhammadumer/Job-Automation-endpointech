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

document.getElementById('toggleButton').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent default anchor behavior
    
    var isPlay = document.getElementById('play').style.display !== 'none'; // Check if Play is visible
    console.log("Play button clicked. Is Play visible?", isPlay); // Debugging line

    // Send a POST request to toggle the dice status
    fetch('/toggle_dice_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: isPlay ? 'start' : 'stop' })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response from server:", data); // Check server response
        if (data.success) {
            // Toggle the button icon visibility
            document.getElementById('play').style.display = isPlay ? 'none' : 'inline';
            document.getElementById('pause').style.display = isPlay ? 'inline' : 'none';
        } else {
            console.error('Error:', data.message);  // Log any error from the server
        }
    })
    .catch(error => console.error('Error:', error));
});