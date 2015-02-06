<?php

  if($_POST)
  {
    $con = mysql_connect("localhost","YOUR_USERNAME","YOUR_PASSWORD");
    if (!$con)
    {
      die('Could not connect: ' . mysql_error());
    }
    mysql_select_db("contacts", $con);
  	
    $query1 = "DROP TABLE IF EXISTS `contacts`.`myo`;";
    mysql_query($query1);

    $query2= "CREATE TABLE `contacts`.`myo`(id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(id),value INT);";
  	mysql_query($query2); 
  	
    mysql_close($con);
    echo "table dropped and created successfully"; 
  }

?>