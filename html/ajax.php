<?php 

function writeToSocket($command){

	$socket = socket_create(AF_UNIX, SOCK_DGRAM, 0);

	socket_connect($socket, "/var/run/python_timelapse_socket");

	socket_write($socket, $command, strlen($command));

	socket_close($socket);

}

switch ($_POST['action']){

    case "turn":

	switch ($_POST['command']){
	    case "right":
			writeToSocket("turn,right");   
    	break;

	    case "left":
			writeToSocket("turn,left"); 
	    break;

	    case "straight":
    		writeToSocket("turn,straight"); 
	    break;

	    case "fineright":
    		writeToSocket("fine,right");
	    break;

	    case "fineleft":
    		writeToSocket("fine,left");
	    break;
	}
	

    break;

    case "move":

	switch ($_POST['command']){
	    case "forward":
			writeToSocket("move,forward");
	    break;

	    case "backward":
			writeToSocket("move,backward");
	    break;

	    case "stop":
			writeToSocket("move,stop");
	    break;
	}

    break;

    case "time":

	switch ($_POST['command']){
	    case "shoottime":
		writeToSocket("shoot,".$_POST['timer']);
	    break;
	}

    break;

}


?>