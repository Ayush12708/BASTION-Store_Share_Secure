document.addEventListener("DOMContentLoaded", function() {

    const loginBtn = document.getElementById("loginBtn");
    const startBtn = document.getElementById("startBtn");

    if (loginBtn) {
        loginBtn.addEventListener("click", function() {
            window.location.href = "login.html";
        });
    }

    if (startBtn) {
        startBtn.addEventListener("click", function() {
            window.location.href = "signup.html";
        });
    }

});