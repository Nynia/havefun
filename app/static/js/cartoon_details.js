var oA = document.getElementsByClassName('say');
console.log(oA);

var oB = document.getElementById('chapter');
console.log(oB);
var oLi = document.querySelectorAll('#chapter li');
console.log(oLi);
var oC = document.querySelector('.photo');
console.log(oC);
var index = -1;
 function ss(){
//	e = e|| window.event
//	e.stopPropagation()
    oB.style.display = oB.style.display =='block' ? 'none' :'block';
    $('.say img').css('transition-duration','0.2'+'s');
    oC.style.transform =oC.style.transform=="rotateX(180deg)" ? '' : 'rotateX(180deg)';
 }



