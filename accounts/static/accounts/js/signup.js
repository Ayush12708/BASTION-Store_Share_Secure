// Show/Hide password
function togglePassword(id) {
    const pwd = document.getElementById(id);
    pwd.type = pwd.type === "password" ? "text" : "password";
}

// Form validation
const form = document.getElementById("signupForm");
form.addEventListener("submit", function(e){
    e.preventDefault();

    const uname = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const pwd = document.getElementById("password").value.trim();
    const confirmPwd = document.getElementById("confirmPassword").value.trim();
    const errorMsg = document.getElementById("errorMsg");
    const signupBtn = document.getElementById("signupBtn");

    errorMsg.textContent = "";

    if(!uname || !email || !pwd || !confirmPwd) {
        errorMsg.textContent = "All fields are required!";
        shake(signupBtn);
        return;
    }

    if(!validateEmail(email)) {
        errorMsg.textContent = "Invalid email address!";
        shake(signupBtn);
        return;
    }

    if(pwd.length < 6) {
        errorMsg.textContent = "Password must be at least 6 characters!";
        shake(signupBtn);
        return;
    }

    if(pwd !== confirmPwd) {
        errorMsg.textContent = "Passwords do not match!";
        shake(signupBtn);
        return;
    }

    // Simulate signup
    signupBtn.disabled = true;
    signupBtn.textContent = "Signing up...";
    setTimeout(() => {
        alert("Account created successfully!");
        window.location.href = "index.html"; // redirect to login
    }, 1200);
});

// Shake effect for errors
function shake(element) {
    element.style.animation = "shake 0.3s";
    element.addEventListener('animationend', () => {
        element.style.animation = '';
    });
}

// Simple email validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email.toLowerCase());
}
document.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", function(e){
        e.preventDefault();
        const target = this.href;

        document.body.style.opacity = "0";
        document.body.style.transition = "0.3s";

        setTimeout(()=>{
            window.location.href = target;
        },300);
    });
});