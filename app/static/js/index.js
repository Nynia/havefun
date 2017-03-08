//轮播图

var index = 0
	var timer
	function show(a){
	    index = a || index
	    if(index<0) index = $('.slide ul li').length-1
	    if(a ==0){index =0}
	    if(index==$('.slide ul li').length) index=0
	    $('.slide ul li').eq(index).fadeIn(800).siblings().hide()
	    $('.slide ul li img').eq(index).css('display','block').siblings().css('display','none')
	    $('.icon span').eq(index).css('background-color','#fff').siblings().css('background-color','#c4c3c9')
	}
	function play(){
	    timer = setInterval(function(){
	        index++
	        show(index)
	    },2500)
	}
	play()
	$('.slide').hover(function(){
	    clearInterval(timer)
	    $('.slide div').show()
	},function(){
	    play()
	    $('.slide div').hide()
	})
	$('.icon span').hover(function(){
	    var $index = $(this).index()
	    show($index)
	})

//游戏热门推荐
$(document).ready(function(){
	$('.recommend_top ul li').hover(function(){
    $(this).find('a').css('color','#eba241').end().siblings().find('a').css('color','#333');
    $(this).find('a').css('font-weight','600').end().siblings().find('a').css('font-weight','normal')
    $index = $(this).index()
    $('.recommend_bottom .part').eq($index).show().siblings().hide()
  })
})

//游戏页面特惠礼包

    $.ajax({
	type:"get",
	url:"http://221.228.17.87/api/v1.0/packages",
	data:{
		type:2,
	},
	dataType:'json',
	success:function(data){
		console.log(data);
        var html = template('data',{data:data.data})
//      console.log(html)
//      console.log(data.data)
		$('#package').html(html)
		console.log(data.data[0].img)
		console.log($("#package ul li"))
		$("#package ul li")[0].onclick = function(){
//			console.log($(this).html())
//			alert(1)
		}
	}
});
//游戏接口
console.log($("#package ul li"))
//热门推荐  推荐指数
    $.ajax({
	type:"get",
	url:"http://127.0.0.1:5000/api/v1.0/games",
	data:{
		type:2,
	},
	dataType:'json',
	success:function(data){
		console.log(data);
		var array=[];
		for(var i=0;i<data.data.length;i++){
			array.push(data.data[i])
			if(i==3){break;}
		}
        var html = template('datas',{datas:array})
        console.log(array)
		$('#role').html(html)

	}
});

   $.ajax({
	type:"get",
	url:"http://221.228.17.87/api/v1.0/packages",
	data:{
		id:10,
	},
	dataType:'json',
	success:function(data){
		console.log(data);
//      var html = template('games',{games:data.data})
//      console.log(html)
//		$('#role').html(html)
	}
});


//var wWidth = (screen.width > 0) ? (window.innerWidth >= screen.width || window.innerWidth == 0) ? screen.width : window.innerWidth : window.innerWidth;
//var wHeight = (screen.height > 0) ? (window.innerHeight >= screen.height || window.innerHeight == 0) ? screen.height : window.innerHeight : window.innerHeight;
//var wFsize = wWidth > 1080 ? 144 : wWidth / 7.2;
//wFsize = wFsize > 32 ? wFsize : 32;
//document.getElementsByTagName('html')[0].style.fontSize = wFsize + 'px';
//document.getElementById("fixed").style.display="none";