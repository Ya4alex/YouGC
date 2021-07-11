// получаем координаты элемента в контексте документа
function getbottom(elem) {
    return elem.getBoundingClientRect().bottom + document.documentElement.scrollTop;
}

function Crop() {
    let border = document.getElementById('border');
    let crop = document.getElementById('crop');
    let delta = getbottom(crop) - getbottom(border);
    
    crop.style.maxHeight = (crop.clientHeight - delta) + 'px';
    
}
document.addEventListener("DOMContentLoaded", Crop);
window.addEventListener('resize', Crop);
