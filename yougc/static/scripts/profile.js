var is_profile_menu_open = false;
function openProfileMenu(){
    if (is_profile_menu_open){
        $("#profile_menu").hide();
        is_profile_menu_open = false;
    }else{
        $("#profile_menu").show();
        is_profile_menu_open = true;
    }
}