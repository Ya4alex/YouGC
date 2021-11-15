function getbottom(elem) {
    return elem.getBoundingClientRect().bottom + document.documentElement.scrollTop;
}

function Crop() {
    let border = document.getElementById('border');
    let crop = document.getElementById('crop');
    let delta = getbottom(crop) - getbottom(border);

    crop.style.maxHeight = (crop.clientHeight - delta) + 'px';

}

$(document).ready(function(){
    if ($(window).width() < 650){
        $('.shop-container').removeClass('shop-container');
        $('.shop-left-side').width('100%');

        $('#laptop-balance').hide();
        $('#mobile-balance').show();

        $('.shop-item').css("margin", "0px 0px 10px 0px");
        $('.shop-item').width('100%');
        $('.shop-items-container').width('100%');

    } else {
        render_catalog();
        window.addEventListener('resize', render_catalog);

        Crop();
        window.addEventListener('resize', Crop);
        document.addEventListener("load", Crop);
        setTimeout(Crop, 1000);
    }
});


