 function preference_menu(){
        const preference_actual = localStorage.getItem("preference_menu_open")
        if (preference_actual && preference_actual==='true'){
            localStorage.setItem("preference_menu_open", "false");
        }else{
            localStorage.setItem("preference_menu_open", "true");
        }
    }