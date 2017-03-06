$(':text').focus(function () { 
    setInterval(function(){
        if($(':text').val().length>0){
            $(':text').next().show()
        }else{
            $(':text').next().hide()
        }
    },20)
}) 
$(':text').next().click(function(){
	$(':text').val('')
})
