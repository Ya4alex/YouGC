jQuery( window ).scroll(function() {
    var pos = jQuery( window ).scrollTop() / 10;
    jQuery('html').css({backgroundPosition: 'left -' + pos + 'px'});
});