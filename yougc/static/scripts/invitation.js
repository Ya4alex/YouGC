function setCookie(name, value, options={}) {
    options = {
        path: '/',
    };

    if (options.expires instanceof Date) {
        options.expires = options.expires.toUTCString();
    }

    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
            updatedCookie += "=" + optionValue;
        }
    }

    document.cookie = updatedCookie;
}
function getCookie(name) {
    let matches = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function copyDiscordLink() {
  var copyText = document.getElementById("discord-link-field");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(copyText.value);
  document.getElementById("show-discord-link-field").textContent="copied!";
}

function swap() {
    if ($('#ticket-info').is(":hidden")) {
        $('#ticket-login').slideUp(400);
        $('#ticket-info').slideDown(400);
        $('#digit').html("3");
    } else {
        $('#ticket-login').slideDown(400);
        $('#ticket-info').slideUp(400);
        $('#digit').html("4");
    }
}

function hideVideo() {
    $('#ticket-show').slideDown(400);
    setCookie('video', '');
    $('#ticket-present').height(0);
    $('nav').css('border-radius', '5px');
}
function showVideo() {
    $('#ticket-show').slideUp(400);
    setCookie('video', 1);
    CropTicket();
    $('nav').css('border-radius', '5px 5px 0px 0px');
}

function getbottom(elem) {
    return elem.getBoundingClientRect().bottom + document.documentElement.scrollTop;
}

function CropTicket() {
    if (getCookie('video')) {
        let crop = document.getElementById('ticket-present');
        let a = innerHeight - getbottom(crop);

        crop.style.height = (crop.clientHeight + a - 9) + 'px';
    }
}

if (getCookie('video') == undefined) {
    setCookie('video', 1);
} else if (!getCookie('video')) {
    hideVideo();
}

document.addEventListener("DOMContentLoaded", CropTicket);
window.addEventListener('resize', CropTicket);
