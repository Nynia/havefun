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
		
     
        
    });
