function buyProduct(server, name, long_name) {
  if (confirm("Вы действительно хотите купить " + long_name + "?")) {
        document.location.href = "/buy/" + server + "/" + name;
    }
}
function render_catalog(){
  var w = $('#crop').width();
  var raw_col = Math.floor(w / 200);
  var car_w = Math.floor((w - (raw_col * 10)) / raw_col);
  $('.shop-item').width(car_w);
}

$('.nav').css("border-radius", "5px");