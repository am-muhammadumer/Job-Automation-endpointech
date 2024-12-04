document.addEventListener('DOMContentLoaded', () => {
    // Format the Expiry Date Input
    const expiryInput = document.getElementById('expiry-date');
    expiryInput.addEventListener('input', (event) => {
        let value = event.target.value.replace(/\D/g, ''); // Remove non-numeric characters
        if (value.length >= 2) {
            value = value.substring(0, 2) + ' / ' + value.substring(2, 4);
        }
        event.target.value = value.substring(0, 7); // Limit to MM / YY format
    });

    // Format Card Number Input
    const cardInput = document.getElementById('card-number');
    cardInput.addEventListener('input', (event) => {
        let value = event.target.value.replace(/\D/g, ''); // Remove non-numeric characters
        value = value.match(/.{1,4}/g)?.join(' ') || ''; // Group in blocks of 4 digits
        event.target.value = value.substring(0, 19); // Limit to 19 characters
    });

    // Disable Autofill
    const formFields = document.querySelectorAll('input');
    formFields.forEach((field) => {
        field.setAttribute('autocomplete', 'new-password');
    });
});
