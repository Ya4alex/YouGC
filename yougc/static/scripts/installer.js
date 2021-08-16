$('.server-block').css("border-radius", "0 0 5px 5px");

function download_installer(instlink){
	var link = document.createElement('a');
	link.setAttribute('href', instlink);
	link.setAttribute('download', instlink);
	link.click();
	return false;
}