function buyProduct(server, name, long_name) {
    if (confirm("Вы действительно хотите купить " + long_name + "?")) {
        document.location.href = "/buy/" + server + "/" + name;
    }
}
function render_catalog() {
    var w = $('#crop').width();
    var raw_col = Math.floor(w / 200);
    var car_w = Math.floor((w - (raw_col * 10)) / raw_col);
    $('.shop-item').width(car_w);
}

$('.nav').css("border-radius", "5px");

var all_info = [];

function info(el) {
    let q = $(el);
    let f = q.is(":hidden");
    $.each(all_info, function(index, href) {
        $(href).hide();
    });
    if (f) {
        q.show();
    } else {
        q.hide();
    }
    if (q.position().left < 0) {
        q.css('left', 0);
    }
    ;if (q.position().left + q.width() > $(window).width()) {
        q.css('right', 0);
    }
}
