// Select the toggle button
const darkModeToggle = document.getElementById("darkModeToggle");

// Check localStorage for user preference
const currentMode = localStorage.getItem("darkMode");
if (currentMode === "enabled") {
    enableDarkMode();
}

// Event Listener for the toggle button
darkModeToggle.addEventListener("click", () => {
    const isDarkModeEnabled = document.body.classList.contains("dark-mode");
    if (isDarkModeEnabled) {
        disableDarkMode();
    } else {
        enableDarkMode();
    }
});

// Enable Dark Mode
function enableDarkMode() {
    document.body.classList.add("dark-mode");
    document.querySelector("header").classList.add("dark-mode");
    document.querySelectorAll("nav a").forEach(link => link.classList.add("dark-mode"));
    document.querySelector("#darkModeToggle").classList.add("dark-mode");
    localStorage.setItem("darkMode", "enabled");
}

// Disable Dark Mode
function disableDarkMode() {
    document.body.classList.remove("dark-mode");
    document.querySelector("header").classList.remove("dark-mode");
    document.querySelectorAll("nav a").forEach(link => link.classList.remove("dark-mode"));
    document.querySelector("#darkModeToggle").classList.remove("dark-mode");
    localStorage.setItem("darkMode", "disabled");
}

// Smooth Scrolling
document.querySelectorAll("a[href^='#']").forEach(anchor => {
    anchor.addEventListener("click", function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute("href")).scrollIntoView({
            behavior: "smooth",
        });
    });
});

// Send Contact Form with EmailJS
document.getElementById("contactForm").addEventListener("submit", function(e) {
    e.preventDefault();

    emailjs
        .send("service_id", "template_id", {
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            message: document.getElementById("message").value,
        })
        .then(
            () => {
                document.getElementById("formMessage").textContent = "Message sent successfully!";
            },
            () => {
                document.getElementById("formMessage").textContent = "Failed to send message. Try again.";
            }
        );
});