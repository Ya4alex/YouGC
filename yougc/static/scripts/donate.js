jQuery(function(e){e.fn.hScroll=function(l){l=l||120,e(this).bind("DOMMouseScroll mousewheel",function(t){var i=t.originalEvent,n=i.detail?i.detail*-l:i.wheelDelta,o=e(this).scrollLeft();o+=n>0?-l:l,e(this).scrollLeft(o),t.preventDefault()})}});


$(document).ready(function(){
    $('#points').hScroll(35); // You can pass (optionally) scrolling amount
});


points_el = $("#points");
function add_points(index, card){
    let d = $('<div>', {"class": 'card-points'});
    d.append($('<div>', {"class": 'price'}).html(card["price"] + "₽"));
    d.append($('<a>').html("купить").attr('href', '/service/donate_pay?type=points&card='+ index.toString()));
    d.css("background-image","url(/static/img/donate/points_coins/" + card["value"].toString() + ".png)");
    points_el.append(d);
}


$.ajax({
    url: "http://127.0.0.1:8000/service/get_donate_configuration",
    success: function(result) {
        var POINTS = result["points"];

        $.each(POINTS, function(index, card) {
            if (card["status"] || !("status" in card)) {
                add_points(index, card);
            }
        });

    }
});
