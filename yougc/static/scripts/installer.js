$('.server-block').css("border-radius", "0 0 5px 5px");

if ($(window).width() < 390){
	$('#laptop').hide();
    $('#mobile').show();

    $('html').css('padding','3% 8%')
}



function download_installer(instlink){
	var link = document.createElement('a');
	link.setAttribute('href', instlink);
	link.setAttribute('download', instlink);
	link.click();
	return false;
}