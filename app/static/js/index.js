//轮播图

    var index = 0;
	var timer;
	function show(a){
	    index = a || index;
	    if(index<0) index = $('.slide ul li').length-1;
	    if(a ==0){index =0};
	    if(index==$('.slide ul li').length) index=0;
	    $('.slide ul li').eq(index).fadeIn(800).siblings().hide();
//	    $('.slide ul li img').eq(index).css('display','block').siblings().css('display','none');
	    $('.slide ul li img').eq(index).css('display','block').siblings().find('div').css('display','block')
	    $('.icon span').eq(index).css('background-color','#fff').siblings().css('background-color','#c4c3c9');
	}
	function play(){
	    timer = setInterval(function(){
	        index++;
	        show(index);
	    },2500)
	}
	play();
	$('.slide').hover(function(){
	    clearInterval(timer);
	    $('.slide div').show();
	},function(){
	    play();
	    $('.slide div').hide();
	})
	$('.icon span').hover(function(){
	    var $index = $(this).index();
	    show($index);
	})
	
//游戏热门推荐
$(document).ready(function(){
	$('.recommend_top ul li').hover(function(){   
    $(this).find('a').css('color','#eba241').end().siblings().find('a').css('color','#333');
    $(this).find('a').css('font-weight','600').end().siblings().find('a').css('font-weight','normal');
    $index = $(this).index();
    $('.recommend_bottom .part').eq($index).show().siblings().hide();
  })
})

//游戏页面特惠礼包

$.ajax({
	type:"get",
	url:"http://221.228.17.87/api/v1.0/packages",
	data:{
		type:2,
	},
	dataType:'jsonp',
	success:function(data){
		console.log(data);
        var html = template('data',{data:data.data})
		$('#package').html(html)
		
		for(var postId = 0;postId<data.data.length;postId++){
			$("#package ul li")[postId].onclick = function(){
				var id=$(this).attr("id")
				location.href="package.html/#"+id	
		
			}
		}
	}
});
   $.ajax({
   	type:""
   });
//游戏接口
console.log($("#package ul li"))
//热门推荐  推荐指数
    $.ajax({
	type:"get",
	url:"http://221.228.17.87/api/v1.0/games", 
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


