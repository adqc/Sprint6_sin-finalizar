<?php
  session_start();

  if (!isset($_SESSION['userID']) || !isset($_SESSION['email'])){
      header('Location: login.php');
      exit();
  }
?>
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Dashboards</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

  </head>
  <body>
    <div class="container" style="margin-top:100px">
      <div class="row justify-content-center">
        <div class="col-md-3" align="center">
          <img src="<?php echo $_SESSION['picture']; ?>">
        </div>
        <div class="col-md-9">
            User ID: <?php echo $_SESSION['userID']; ?><br>
            Name: <?php echo $_SESSION['name']; ?><br>
            Email> <?php echo $_SESSION['email']; ?><br>
        </div>
      </div>
    </div>
  </body>
</html>
