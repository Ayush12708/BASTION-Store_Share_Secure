// Show/Hide password
function togglePassword() {
    const pwd = document.getElementById("password");
    pwd.type = pwd.type === "password" ? "text" : "password";
}

// On page load, fill username if saved
window.onload = function() {
    const savedUser = localStorage.getItem("username");
    if(savedUser) {
        document.getElementById("username").value = savedUser;
        document.getElementById("remember").checked = true;
    }
}

// Form validation + fake login simulation
const form = document.getElementById("loginForm");
form.addEventListener("submit", function(e) {
    e.preventDefault(); // prevent default form submission

    const uname = document.getElementById("username").value.trim();
    const pwd = document.getElementById("password").value.trim();
    const remember = document.getElementById("remember").checked;
    const errorMsg = document.getElementById("errorMsg");
    const loginBtn = document.getElementById("loginBtn");

    errorMsg.textContent = ""; // reset error

    if(!uname || !pwd) {
        errorMsg.textContent = "Please enter both username and password!";
        return;
    }

    // Save username if "Remember me" checked
    if(remember) {
        localStorage.setItem("username", uname);
    } else {
        localStorage.removeItem("username");
    }

    // Simulate login (replace with real AJAX)
    loginBtn.disabled = true;
    loginBtn.textContent = "Logging in...";
    setTimeout(() => {
        if(uname === "admin" && pwd === "1234") { // fake credentials
            alert("Login successful!");
            window.location.href = "/dashboard.html"; // redirect
        } else {
            errorMsg.textContent = "Invalid username or password!";
            loginBtn.disabled = false;
            loginBtn.textContent = "Login";
        }
    }, 1500);
});
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