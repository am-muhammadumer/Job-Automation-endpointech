
    document.addEventListener('DOMContentLoaded', function () {
        const burgerMenu = document.querySelector('.burgerMenu');
        const burgerMenuDropdown = document.querySelector('.burgerMenuDropdown');

        // Toggle the dropdown when the burger menu is clicked
        burgerMenu.addEventListener('click', () => {
            // Toggle the visibility of the dropdown
            burgerMenuDropdown.classList.toggle('active');

            if (burgerMenuDropdown.classList.contains('active')) {
                burgerMenuDropdown.style.display = 'block';
                setTimeout(() => {
                    burgerMenuDropdown.style.opacity = '1';
                    burgerMenuDropdown.style.transform = 'translateY(0)';
                }, 10);
            } else {
                burgerMenuDropdown.style.opacity = '0';
                burgerMenuDropdown.style.transform = 'translateY(-10px)';
                setTimeout(() => {
                    burgerMenuDropdown.style.display = 'none';
                }, 300); // Wait for transition to complete before hiding
            }
        });

        // Close the dropdown if clicked outside
        window.addEventListener('click', (e) => {
            if (!burgerMenu.contains(e.target) && !burgerMenuDropdown.contains(e.target)) {
                burgerMenuDropdown.style.opacity = '0';
                burgerMenuDropdown.style.transform = 'translateY(-10px)';
                setTimeout(() => {
                    burgerMenuDropdown.style.display = 'none';
                }, 300);
            }
        });
    });


    // Get the button element
    const backToTopBtn = document.getElementById('backToTopBtn');

    // When the user clicks on the button, scroll to the top of the page
    backToTopBtn.addEventListener('click', function () {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'  // Smooth scroll effect
        });
    });

    // Optionally, you can make the button appear only after scrolling a certain distance
    window.onscroll = function () {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
            backToTopBtn.style.display = 'block';  // Show button when scrolled 300px
        } else {
            backToTopBtn.style.display = 'none';   // Hide button when at the top
        }
    };

    // Get elements
    const profileBtn = document.getElementById('profileBtn');
    const dropdown = document.querySelector('.dropdown');

    // Toggle dropdown on click
    profileBtn.addEventListener('click', () => {
        if (dropdown.style.display === 'block') {
            dropdown.style.display = 'none'; // Hide if already shown
            dropdown.style.opacity = '0';
            dropdown.style.transform = 'translateY(-10px)';
        } else {
            dropdown.style.display = 'block'; // Show the dropdown
            setTimeout(() => {
                dropdown.style.opacity = '1';
                dropdown.style.transform = 'translateY(0)';
            }, 10); // Delay for smooth animation
        }
    });

    // Close dropdown if clicked outside
    window.addEventListener('click', (e) => {
        if (!profileBtn.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
            dropdown.style.opacity = '0';
            dropdown.style.transform = 'translateY(-10px)';
        }
    });

