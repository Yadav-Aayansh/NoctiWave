const body = document.querySelector('body'),
      sidebar = body.querySelector('nav'),
      toggle = body.querySelector(".toggle"),
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text");


toggle.addEventListener("click" , () =>{
    sidebar.classList.toggle("close");
})

modeSwitch.addEventListener("click" , () =>{
    body.classList.toggle("dark");
    
    if(body.classList.contains("dark")){
        modeText.innerText = "Light mode";
    }else{
        modeText.innerText = "Dark mode";
        
    }
});


//thoda sa aur js top_nav ke liye
window.addEventListener("scroll", function(){
    let top_nav = document.querySelector(".top_nav")
    top_nav.classList.toggle("fix_top_nav", window.scrollY>0);

})

//notification ke liye

notif= document.querySelector('.notification_icon');


notif.addEventListener('click', function(){
    notif_box= document.querySelector('.notification_box_top')
    if(notif_box.classList.contains('show')){
        notif_box.classList.remove('show')
    }
    else{
        notif_box.classList.add('show')
    }
});