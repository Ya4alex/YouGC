if ($(window).width() < 670){
    $('.shop-container').removeClass('shop-container');
    $('.shop-left-side').width('100%');
    
    $('#laptop-balance').hide();
    $('#mobile-balance').show();

    $('.shop-item').css("margin", "0px 0px 10px 0px");
    $('.shop-item').width('100%');
    $('.shop-items-container').width('100%');

} else {
    document.addEventListener("DOMContentLoaded", render_catalog);
    window.addEventListener('resize', render_catalog);

    document.addEventListener("DOMContentLoaded", Crop);
    window.addEventListener('resize', Crop);
}