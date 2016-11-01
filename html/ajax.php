<?php 

function writeToSocket($command){

	$socket = socket_create(AF_UNIX, SOCK_DGRAM, 0);

	socket_connect($socket, "/var/run/python_timelapse_socket");

	socket_write($socket, $command, strlen($command));

	socket_close($socket);

}

if ($_POST['action'] == "command"){
	writeToSocket($_POST['command'].",".$_POST['value']);   
}

?>