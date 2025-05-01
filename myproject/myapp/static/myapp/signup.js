document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signup-form");
    const messageParagraph = document.getElementById("message");
  
    signupForm.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the default form submission
  
      // Retrieve and trim field values
      const username = document.getElementById("username").value.trim();
      const place = document.getElementById("place").value.trim();
      const dob = document.getElementById("dob").value;
      const gender = document.getElementById("gender").value;
      const email = document.getElementById("email").value.trim();
      const contact = document.getElementById("contact").value.trim();
  
      // Basic required fields validation
      if (!username || !place || !dob || !gender || !email || !contact) {
        messageParagraph.textContent = "Please fill all the required fields.";
        messageParagraph.style.color = "red";
        return;
      }
  
      // If validation passes, display a success message and simulate form submission
      messageParagraph.textContent = "Signup successful! Redirecting...";
      messageParagraph.style.color = "green";
  
      // Simulate a delay before redirect (for example, 1.5 seconds)
      setTimeout(function () {
        window.location.href = "index.html";
      }, 1500);
    });
  });
  