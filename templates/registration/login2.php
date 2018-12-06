<!DOCTYPE html>
<?php
  session_start();

  if (isset($_POST['userID'])){
    $_SESSION['userID']=$_POST['userID'];
    $_SESSION['accessToken']=$_POST['accessToken'];
    $_SESSION['email']=$_POST['email'];
    $_SESSION['name']=$_POST['name'];
    $_SESSION['picture']=$_POST['picture'];
    exit("success");
  }

?>
<html lang="en" dir="ltr">
<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

  <title>Hello, world!</title>
</head>
  <body>
    <div class="container" style="margin-top:100px">
      <div class="row justify-content-center">
        <div class="col-md-6 col-offset-3" align="center">
          <form>
            <input type="form-control" placeholder="Usuario"><br>
            <input type="form-control" placeholder="Contraseña"><br>
            <input class="btn btn-primary" type="submit"  value="Log In">
            <input class="btn btn-primary" type="button" onclick="logIn()"  value="Log In with Facebook">
          </form>
        </div>
      </div>
    </div>

  <script
    src="https://code.jquery.com/jquery-3.3.1.min.js"
    integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
    crossorigin="anonymous">
  </script>

  <script>
    var person = { userID: "", name: "", accessToken: "", email: "", picture:""};
    function logIn(){
      FB.login(function (response){
        if (response.status=="connected"){
            person.userID=response.authResponse.userID;
            person.accessToken=response.authResponse.accessToken;

            FB.api('/me?fields=id,name,first_name,last_name,email,picture.type(large)',function (userData){
                console.log(userData);
                person.name=userData.name;
                person.email=userData.email;
                person.picture = userData.picture.data.url;

                $.ajax({
                  url:"login2.php",
                  method:"POST",
                  data:person,
                  dataType: 'text',
                  success: function (serverResponse){
                    if (serverResponse == "success"){
                        window.location = "login3.php";
                    }
                  }
                })
            });
        }
      }, {scope: 'public_profile, email'})
    }
    window.fbAsyncInit = function() {
      FB.init({
        appId            : '733662990335277',
        autoLogAppEvents : true,
        xfbml            : true,
        version          : 'v3.2'
      });
    };

    (function(d, s, id){
       var js, fjs = d.getElementsByTagName(s)[0];
       if (d.getElementById(id)) {return;}
       js = d.createElement(s); js.id = id;
       js.src = "https://connect.facebook.net/en_US/sdk.js";
       fjs.parentNode.insertBefore(js, fjs);
     }(document, 'script', 'facebook-jssdk'));
  </script>
  </body>
</html>
