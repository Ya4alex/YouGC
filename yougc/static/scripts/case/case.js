$("#html").addClass("hide-scroll");

var Rarity = {
    'обычный': '#fff',
    'редкий': '#16A64A',
    'уникальный': '#633DFF',
    'мифический': '#E0E345',
    'легендарный': '#B64BE6',
    'секретный': '#FF113F',
};

var CaseConf = [];
var fakeDrop = [];

var AnyCases = true;
var Reseted = false;
var CaseChosen = 0;

var roulette_div = $("#roulette");
var cards_window = $("#open-case-window");
var cards_block = $('#open-case-container');

var cases_div = $("#cases-container");
var drop_div = $("#drop-container");

$.ajax({
    url: "/service/get_user_cases",
    data: {
        "random": Math.random()
    },
    success: function(result) {
        CaseConf = result;
        $.each(result, function(index, card) {
            if (card) {
                p = $("<div>", {
                    "class": "case unselectable",
                    "style": "background-image: url(/static/img/case/cases/" + (index + 1) + ".png);",
                    "onclick": "openCase(" + (index + 1) + ")",
                    "id": "case" + (index + 1)
                });
                p.append($("<span>" + card + "</span>"));
                cases_div.append(p);
                if (CaseChosen == 0) {
                    CaseChosen = p;
                    p.addClass("case-choise");
                }
            }
        });
        if (CaseChosen == 0) {
            AnyCases = false;
        }
    }
});

$.ajax({
    url: "/service/get_fake_drop",
    data: {
        "random": Math.random(),
    },
    success: function(result) {
        fakeDrop = result;
    }
});

function random(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
}

async function loadDrop() {
    drop_div.empty();
    ch = getCaseChosenID();
    local_fake_drop = fakeDrop[ch - 1];

    fake_points = local_fake_drop['pnt'];
    fake_ather = local_fake_drop['txtr'];

    if (!$.isEmptyObject(fake_points)) {
        p = $("<div>", {
            "class": "drop-card drop-points"
        });
        p.append($("<span>", {
            "class": "text-points"
        }).html(fake_points[0] + '-' + (fake_points[1] + 1)));
        p.css({
            "background-image": "url(/static/img/case/staff/points.png?v=1)",
            "filter": "drop-shadow(0 0 10px #fff)"
        });
        drop_div.append(p);
    }
    if (!$.isEmptyObject(fake_ather)) {
        $.each(fake_ather, function(index, data) {
            p = $("<div>", {
                "class": "drop-card drop-texture"
            });
            p.append($("<span>", {
                "class": "text-texture"
            }).html(data['ln']));
            p.css({
                "background-image": "url(/static/img/shop/" + data['n'] + ".png?v=1)",
                "filter": "drop-shadow(0 0 10px " + Rarity[data['rt']] + ")"
            });
            drop_div.append(p);
        });
    }
}

async function reset() {
    cards_block.empty();
    for (let i = 0; i < 60; i++) {
        cards_block.append($("<div>", {
            "class": "card",
            "id": "box" + i
        }))
    }
    var cards = cards_block.children();

    ch = getCaseChosenID();

    local_fake_drop = fakeDrop[ch - 1];
    k_local_fake_drop = Object.keys(local_fake_drop);

    fake_points = local_fake_drop['pnt'];
    fake_ather = local_fake_drop['txtr'];

    $.each(cards, function(index, card) {
        r = k_local_fake_drop[random(0, k_local_fake_drop.length)];
        switch (r) {
        case 'pnt':
            v = random(fake_points[0], fake_points[1] + 1);
            $(this).append($("<span>", {
                "class": "text-points"
            }).html(v));
            $(this).css({
                "background-image": "url(/static/img/case/staff/points.png?v=1)",
                "filter": "drop-shadow(0 0 5px #fff)"
            });
            break
        case 'txtr':
            _r = random(0, fake_ather.length);
            $(this).css({
                "background-image": "url(/static/img/shop/" + fake_ather[_r]['n'] + ".png?v=1)",
                "filter": "drop-shadow(0 0 10px " + Rarity[fake_ather[_r]['rt']] + ")"
            });
            $(this).addClass('card-texture');
        default:
            break
        }
    });
    Reseted = true;
}

function spin() {
    if (!Reseted) {
        reset();
    }
    var rand = Math.floor(random(1500, (106) * 54) / 106);
    var result = {};
    Cid = getCaseChosenID();
    remooveCase(Cid);

    win = $("#box" + rand);
    win.removeClass();
    win.addClass('card');

    $("#button-spin").attr('disabled', 'disabled');

    $.ajax({
        url: "/service/open_case",
        data: {
            "random": Math.random(),
            "case": Cid,
        },
        success: function(res) {
            result = res;
            win.empty();
            switch (result["typ"]) {
            case 'points':
                win.append($("<span>", {
                    "class": "text-points"
                }).html(result["txt"]));
                win.css({
                "background-image": "url(/static/img/case/staff/points.png?v=2)",
                                "filter": "drop-shadow(0 0 10px #fff)"

                });
                break

            case 'texture':
                win.addClass("card-texture");
                win.css({
                    "background-image": "url(/static/img/shop/" + result['img'] + "?v=1)",
                    "filter": "drop-shadow(0 0 10px " + Rarity[fake_ather[_r]['rt']] + ")"

                });
                break

            default:
                break
            }
        }
    });
    Reseted = false;
    px_rand = (rand - 2) * 106 + 13 + random(0, 90) - 45;
    $("#open-case-container").children().first().animate({
        marginLeft: -px_rand
    }, 8000, function() {
        win.addClass("win");
        switch (result["typ"]) {
        case 'points':
            break

        case 'texture':
            win.append($("<span>", {
                "class": "text-texture"
            }).html(result["txt"]));
            break

        default:
            break
        }
        if (AnyCases) {
            $('#button-spin').removeAttr('disabled');
        }
    });
}

function getCaseChosenID() {
    val = CaseChosen.attr('id');
    return parseInt(val.slice(4), 10);
}

function openCase(id) {
    CaseChosen.removeClass("case-choise");
    CaseChosen = $("#case" + id);
    CaseChosen.addClass("case-choise");
    reset();
    loadDrop();
    openRoulette(true);
}
function remooveCase(id) {
    CaseConf[id - 1] -= 1;
    val = CaseConf[id - 1];

    if (val == 0) {
        CaseChosen.removeClass("case-choise");
        CaseChosen.fadeOut(300);
        CaseChosen = 0;
        res = CaseConf.find(function(x) {
            return x > 0
        });
        if (res === undefined) {
            AnyCases = false;
            alert("no Cases");
            return;
        }
        CaseChosen = $("#case" + (CaseConf.indexOf(res) + 1));
        CaseChosen.addClass("case-choise");
    } else {
        CaseChosen.children().first().html(val);
    }
}

var ISOPEN = false;

$("#button-back-cases").click(openRoulette);
function openRoulette(open=false) {
    if (open == true && ISOPEN == true) {
        return
    }
    $(this).toggleClass("open");
    if (ISOPEN) {
        $(".arrow-button-back-cases").animate({
            marginLeft: '-9px'
        }, 500, function() {
            $("#button-back-cases").hide();
        });

        roulette_div.slideUp(500);
        ISOPEN = false;

            cases_div.slideDown(500);
        drop_div.slideUp(500);
    } else {
        $("#button-back-cases").show();
        $(".arrow-button-back-cases").animate({
            marginLeft: '10px'
        }, 500, function() {
            $("#button-back-cases").show();
        });

        roulette_div.slideDown(500);
        ISOPEN = true;

        cases_div.slideUp(500);
        drop_div.slideDown(500);

    }
}
