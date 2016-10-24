function move(id){
    
	    $.ajax({
		type: "POST",
		url: "/ajax.php",
		data: "action=move&command=" + id,
		success: function(back){
	
		}
	    });

}

function turn(id){
    
	    $.ajax({
		type: "POST",
		url: "/ajax.php",
		data: "action=turn&command=" + id,
		success: function(back){
	
		}
	    });

}

function writeTimer(){

    var timer = $('#timer').val();

    $.ajax({
		type: "POST",
		url: "/ajax.php",
		data: "action=time&command=shoottime&timer=" + timer,
		success: function(back){
	
		}
	    });

}