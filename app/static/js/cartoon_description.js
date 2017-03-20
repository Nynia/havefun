$(function(){
	$('.next').click(function(){
		$('.orderby ul').css('margin-left','50%')
		$('.orderby  ul').stop().animate({marginLeft:'0px'},800)
		$('.orderby ul li').eq(1).insertBefore($('.orderby ul li').eq(0))
	})
	
	$('.orderby a').hover(function(){
		$(this).css('color','#F7D631').siblings().css('color','#fff')
		$index = $(this).index()
		$('.chapter .session').eq($index).show().siblings().hide()
	})
	var a = document.querySelector('dd p').clientHeight
	console.log(a)
	if(a<=40){
	     $('dd a').hide()
	}
})
