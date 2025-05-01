// Toggle visibility of password fields
function togglePassword(id, toggleBtnId) {
    const input = document.getElementById(id);
    const btn = document.getElementById(toggleBtnId);
    if (input.type === "password") {
        input.type = "text";
        btn.innerText = "Hide";
    } else {
        input.type = "password";
        btn.innerText = "Show";
    }
}

// Validate email and password match
function validateSignupForm(event) {
    const pw1 = document.querySelector("input[name='password1']");
    const pw2 = document.querySelector("input[name='password2']");
    if (pw1 && pw2 && pw1.value !== pw2.value) {
        alert("Passwords do not match!");
        event.preventDefault();
    }

    const email = document.querySelector("input[name='email']");
    if (email && !email.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
        alert("Please enter a valid email address.");
        event.preventDefault();
    }
}

// Toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    const current = document.body.classList.contains("dark-mode");
    localStorage.setItem("darkMode", current); // Remember choice
}

// Apply dark mode on load if previously set
window.onload = function () {
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark-mode");
    }
};
