 $(function(){
        var off = true;
        $(".classify_right").click(function(){
            if(off){
                $(this).addClass("on");
                $(".classify_right span").eq(1).css('color','#fff')
                $(".classify_right span").eq(0).css('color','#e9766f')
                off = false;
            }else {
                $(this).removeClass("on");
                $(".classify_right span").eq(0).css('color','#fff')
                $(".classify_right span").eq(1).css('color','#e9766f')
                off = true;
            }
        });
        
//      点击全部的时候,“全部”背景色改变
//      其他项只有一个边框
        $('.all').click(function(){
        	$(this).css('background','#c746fc')
        	$(this).css('color','#fff')
        	for(var i = 0;i<$('.lis').length;i++){
        		$('.lis').css('border','1px solid #f00')
        	} 
        })
        var len =$('.lis').length
		for(var i = 0;i<len;i++){
			$(".lis").eq(i).click(function(){
			if(!$(this).hasClass("ones")){
				$(this).toggleClass("ones");
			} else {
				$(".all").css("background-color","none");
				$(this).toggleClass("ones");
			}
			}) 
			var a = 0;
			if($(".lis").eq(i).hasClass("ones")){
    		a++;
    		if(a == 6) {
    			$(".all").css("background-color","orange");
    		}  else {
	    		$(".all").css("background-color",'none');
	    	}
	    	} else {
	    		$(".all").css("background-color",'none');
	    	}
     }
		
//   轮播图
     //轮播图

//  var index = 0;
//	var timer;
//	function show(a){
//	    index = a || index;
//	    if(index<0) index = $('.slide ul li').length-1;
//	    if(a ==0){index =0};
//	    if(index==$('.slide ul li').length) index=0;
//	    $('.slide ul li').eq(index).fadeIn(800).siblings().hide();
//	    $('.slide ul li img').eq(index).css('display','block').siblings().css('display','none')
//	    $('.icon span').eq(index).css('background-color','#fff').siblings().css('background-color','#c4c3c9');
//	}
//	function play(){
//	    timer = setInterval(function(){
//	        index++;
//	        show(index);
//	    },2500)
//	}
//	play();
//	$('.slide').hover(function(){
//	    clearInterval(timer);
//	    $('.slide div').show();
//	},function(){
//	    play();
//	    $('.slide div').hide();
//	})
//	$('.icon span').hover(function(){
//	    var $index = $(this).index();
//	    show($index);
//	})
    });
