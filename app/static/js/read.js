 $(function(){
//        $(".box span").click(function(){
//            $(this).addClass("on").siblings().removeClass("on")
//        });
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
//
//      
        for(var i = 0;i<$('.lis').length;i++){
        	console.log($('.lis').length)
        	console.log(2)
        	$('.lis').click(function(){
        		$(this).css('background','orangered')
        		$('.all').css('background','#fff')
        		$('.all span').css('color','#c64bf6')
        	})
        }
        $('.lists li').click(function(){
        	console.log(1)
        	$(this).addClass("ons").siblings().removeClass("ons")
        })

        
        
        
    });
