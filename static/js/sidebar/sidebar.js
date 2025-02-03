    const btn_menu = document.querySelector('#bnt-menu')
    const menu = document.querySelector('#menu-side-el')

    const actual_state = localStorage.getItem("preference_menu_open")
           if(actual_state){
                menu.setAttribute('open',actual_state);
           }else{
                menu.setAttribute('open','false');
           }
    if (window.innerWidth <= 500) {
       menu.setAttribute('open','false');
    }

    btn_menu.addEventListener('click', function(){
       const actual_state = menu.getAttribute('open')
       if(actual_state ==='true'){
           menu.setAttribute('open','false');
       } else{
           menu.setAttribute('open','true');
       }
    });