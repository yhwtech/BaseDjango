let bars = document.querySelector(".bars");
bars.onclick = function(){
    let nav = document.querySelector(".navbar");
    nav.classList.toggle("show");
    nav.classList.toggle("active");
}


let circle_account = document.querySelector("#user_circle");
let modal_account = document.querySelector("#modal_account");
modal_account.setAttribute("visibility","hidden")
modal_account.style.display="none"
circle_account.onclick = function(){

        const is_visible= modal_account.getAttribute("visibility") === "visible";
        if(is_visible){
            modal_account.style.display="none"
            modal_account.setAttribute("visibility","hidden")
        }else{
            modal_account.style.display="block"
            modal_account.setAttribute("visibility","visible")
        }
        const circleRect = circle_account.getBoundingClientRect();
        let modalTop = circleRect.bottom + window.scrollY;
        let modalLeft = circleRect.left + window.scrollX;

        const modalWidth = modal_account.offsetWidth;
        const modalHeight = modal_account.offsetHeight;

        if (modalLeft + modalWidth > window.innerWidth) {
            modalLeft = window.innerWidth - modalWidth - 15;
        }

        if (modalTop + modalHeight > window.innerHeight) {
            modalTop = circleRect.top + window.scrollY - modalHeight - 15;
        }
        modal_account.style.top = `${modalTop}px`;
        modal_account.style.left = `${modalLeft}px`;
}