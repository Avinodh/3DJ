<?php

  $con = mysql_connect("localhost","YOUR_USERNAME","YOUR_PASSWORD");

    if (!$con)
    {
      die('Could not connect: ' . mysql_error());
    }

    mysql_select_db("contacts", $con);


  if($_POST)
  {
    $vertical = mysqli_real_escape_string($con,$_POST['vertical']);
    $query = "INSERT INTO `contacts`.`myo` (`id`, `value`) VALUES (NULL, '$vertical');";
    mysql_query($query);
    mysql_close($con);
    header("Status: 200 OK");
  }

  if($_GET)
  {
      $query1 = "SELECT * FROM `contacts`.`myo` ORDER BY `id` DESC LIMIT 1"; 
      $result1= mysql_query($query1); 
      $row = mysql_fetch_row($result1);

      $num_rows = mysql_num_rows($result1);
      if($num_rows==0){
         echo "no-data"; }
      $value = $row[1]; 

      echo $value; 
  }

?>
