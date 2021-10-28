jQuery(function(e) {
    e.fn.hScroll = function(l) {
        l = l || 120,
        e(this).bind("DOMMouseScroll mousewheel", function(t) {
            var i = t.originalEvent
              , n = i.detail ? i.detail * -l : i.wheelDelta
              , o = e(this).scrollLeft();
            o += n > 0 ? -l : l,
            e(this).scrollLeft(o),
            t.preventDefault()
        })
    }
});

$(document).ready(function() {
    $('#points').hScroll(35);
    $('#other').hScroll(35);
    // You can pass (optionally) scrolling amount
});

points_el = $("#points");
function add_points(index, card) {
    let d = $('<div>', {
        "class": 'card-points'
    });
    d.append($('<div>', {
        "class": 'price'
    }).html(card["price"] + "₽"));
    d.append($('<a>').html("купить").attr('href', '/service/donate_pay?type=points&card=' + card['id'].toString()));
    d.css("background-image", "url(/static/img/donate/points_coins/" + card["value"].toString() + ".png)");
    points_el.append(d);
}

$.ajax({
    url: "/service/get_donate_configuration",
    success: function(result) {
        var POINTS = result["points"];

        var POINTS_ = POINTS.sort(function(a, b) {
            if (a['place_id'] < b['place_id']) {
                return -1;
            } else {
                return 1;
            }
        })

        $.each(POINTS_, function(index, card) {
            if (card["status"] || !("status"in card)) {
                add_points(index, card);
            }
        });
    }
}); 

var all_info = ["#info-window-my_name", "#info-window-my_prefix", "#info-window-my_texture"];

function info(el){
    let q = $(el);
    let f = q.is(":hidden");
    $.each(all_info, function(index, href) {$(href).hide();});
    if (f){
        q.show();
    }else{
        q.hide();
    }
    if (q.position().left < 0){q.css('left', 0);};
    if (q.position().left + q.width() > $( window ).width()){q.css('right', 0);}
}
