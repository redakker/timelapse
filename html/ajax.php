<?php 

function writeToFile($action, $value){

    $myfile = "";

    if ($action == "turn"){
	$myfile = fopen("/tmp/direction", "w") or die("Unable to open file!");
    }

    if ($action == "move"){
	$myfile = fopen("/tmp/speed", "w") or die("Unable to open file!");
    }

    if ($action == "fine"){
	$myfile = fopen("/tmp/finetune", "w") or die("Unable to open file!");
    }

    if ($action == "shoottime"){
	$myfile = fopen("/tmp/shoottime", "w") or die("Unable to open file!");
    }

    if ($myfile != ""){
	$txt = $value;
	fwrite($myfile, $txt);
	fclose($myfile);
    }

}

switch ($_POST['action']){

    case "turn":

	switch ($_POST['command']){
	    case "right":
		writeToFile("turn", "1");	    
    	    break;

	    case "left":
		writeToFile("turn", "-1");
	    break;

	    case "straight":
    		writeToFile("turn", "0");
	    break;

	    case "fineright":
    		writeToFile("fine", "1");
	    break;

	    case "fineleft":
    		writeToFile("fine", "-1");
	    break;
	}
	

    break;

    case "move":

	switch ($_POST['command']){
	    case "forward":
		writeToFile("move", "1");
	    break;

	    case "backward":
		writeToFile("move", "-1");
	    break;

	    case "stop":
		writeToFile("move", "0");
	    break;
	}

    break;

    case "time":

	switch ($_POST['command']){
	    case "shoottime":
		writeToFile("shoottime", $_POST['timer']);
	    break;
	}

    break;

}


?>