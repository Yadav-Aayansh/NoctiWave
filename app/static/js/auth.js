let pw_eye = document.querySelector(".pw_eye");
let eye_close = document.querySelector(".pw_eye_close");
let eye_open = document.querySelector(".pw_eye_open");
let password_input = document.querySelector("#password");
let confirm_password_input = document.querySelector("#confirm_password");

eye_close.style.display = "block";
eye_open.style.display = "none";

pw_eye.addEventListener("click", function() {
    if (eye_close.style.display === "block") {
        eye_close.style.transition = "all 0.6s";
        eye_close.style.display = "none";
        eye_open.style.display = "block";
        password_input.type = "text";
        confirm_password_input.type = "text";
    } else {
        password_input.type = "password";
        confirm_password_input.type = "password";
        eye_close.style.display = "block";
        eye_open.style.display = "none";
        console.log("done2");
    }
});


let menu_bar = document.querySelector(".menu_btn");
let menu_bar_open = document.querySelector(".open_menu");
let menu_bar_close = document.querySelector(".close_menu");


menu_bar.addEventListener("click", function () {
    if (menu_bar_open.style.display === "block") {
        menu_bar_open.style.display = "none";
        menu_bar_close.style.display = "block";
    } else {
        menu_bar_open.style.display = "block";
        menu_bar_close.style.display = "none";
    }
});