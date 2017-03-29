$(function(){
	var a = document.querySelector('dd p').innerText.length
	console.log(a)
   if(a>=45){
	   	var b = $('dd p').html();
		var c = b.substr(0,47) + '...';
		$('#intro_short p').text(c);
		$('#intro_short a').show();
   }else{
   	$('#intro_short a').hide();
   }
   
})
