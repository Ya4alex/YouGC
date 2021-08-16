if ($(window).width() < 715){
    $('.left-block').addClass('center-block');
    $('.left-block').removeClass('left-block');

    $('.right-block').addClass('center-block');
    $('.right-block').removeClass('right-block');

    $('.server-slide-block').removeClass('server-slide-block');
    $('.server-players-block').removeClass('server-players-block');

    $('html').css('padding','3% 8%')
}

