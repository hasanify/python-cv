<?php  

include 'db.php';  

$file_name = rand().'_'.basename($_FILES['file']['name']);
$uploaddir = 'cv/';
$uploadfile = $uploaddir . $file_name;
move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile);

$query = "INSERT INTO entries (cv_path) VALUES ('$file_name')";  
if(mysqli_query($conn, $query))
echo "Success";
?> 