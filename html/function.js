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

function writeTimer(time){

    $.ajax({
		type: "POST",
		url: "/ajax.php",
		data: "action=time&command=shoottime&timer=" + time,
		success: function(back){
	
		}
	    });
}

function command(command,value) {

	$.ajax({
		type: "POST",
		url: "/ajax.php",
		data: "action=command&command=" + command + "&value=" + value,
		success: function(back){
	
		}
	    });

}