function convert(x) {
    return new Date(Math.floor(((new Date()).getTime() / 1000) - x) * 1000).toISOString().substr(11, 8);
}

online_container = $("#online_container");
online_counter = $("#online_counter");
function set_time(person, jtime) {
    let d = $('<tr>', {
        "id": person
    });
    d.append($('<td>', {
        "class": 'label'
    }).html(person));
    d.append($('<td>', {
        "class": 'status'
    }).html(convert(jtime)));
    online_container.append(d);
}

var ONLINE = {};

function update() {
    $.each(ONLINE, function(person, jtime) {
        per = $("#" + person);
        per.children().eq(1).text(convert(jtime));
    });
}
var interv = setInterval(update, 1000000);
function load() {
    $.ajax({
        url: "/service/get_server_online",
        data: {
            "server": server_name
        },
        success: function(result) {
            online_counter.text("Игроков онлайн: " + Object.keys(result).length);
            clearInterval(interv);
            online_container.empty();
            $.each(result, function(person, jtime) {
                result[person] = parseInt(jtime);
                set_time(person, parseInt(jtime));
            });
            ONLINE = result;
            interv = setInterval(update, 1000);
            Crop();
        }
    });
    
}

load();
setInterval(load, 10000);
