//游戏接口


$.ajax({
	type:"get",
	url:"http://221.228.17.87/api/v1.0/packages",
	data:{
		type:2,
	},
	dataType:'json',
	success:function(data){
		console.log(data)
		console.log(data.data.slice(0,4))

	}
})



var id = location.hash.substring(1)
$.ajax({
	type:"get",
	url:"http://221.228.17.87/api/v1.0/packages/"+id,
	data:{
		type:2,
	},
	dataType:'jsonp',
	success:function(data){
		console.log(data)
        var html = template('data',{data:data.data}) 
//      console.log(html)
		$('#packages').html(html)
	}

})

//订购
    $('.super button').click(function(){
    	$('#main').show()
    })
    $('.order_bottom .cancel').click(function(){
    	$('#main').hide()
    })
    $('.order_bottom .confirm').click(function(){
    	$('#main').hide()
    	
    	$.ajax({
    		type:"post",
    		url:"",
    		data:{
    			 spid,
    			 chargeid,
    			 secret,
    			 phonenum,
    			 productid
    		},
    		dataType:'json',
    		success:function(data){
    			console.log(data)
    			$('#mains').show()
    		}
    	})
    	
    })


