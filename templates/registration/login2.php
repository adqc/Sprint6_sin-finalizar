<?php
  session_start();
  $_SESSION['userID']=$_POST['userID'];
  $_SESSION['accessToken']=$_POST['accessToken'];
  $_SESSION['email']=$_POST['email'];
  $_SESSION['first_name']=$_POST['first_name'];
  $_SESSION['last_name']=$_POST['last_name'];
  exit("success");
?>
<!DOCTYPE html>
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
            {% csrf_token %}
            <input type="text" id="usuario" placeholder="Usuario" ><br>
            <input type="text" id="email" placeholder="Email"><br>
            <input type="text" id="nombre" placeholder="Nombre"><br>
            <input type="text" id="apellido" placeholder="Apellido"><br>
            <input type="text" placeholder="Contraseña"><br>
            <div id= "holi"></div>
            <br></br>
            <input class="btn btn-primary" type="submit"  value="Log In">
            <input class="btn btn-primary" type="button" onclick="logIn()" value="Log In with Facebook">
          </form>
        </div>
      </div>
    </div>

  <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>


  <script>


    var person = { userID: "", first_name: "", last_name:"", accessToken: "", email: ""};
    function logIn(){

      FB.login(function (response){
        if (response.status=="connected"){
            person.userID=response.authResponse.userID;
            person.accessToken=response.authResponse.accessToken;

            FB.api('/me?fields=id,first_name, last_name, email',function (userData){
                console.log(userData);
                person.first_name=userData.first_name;
                person.last_name=userData.last_name;
                person.email=userData.email;
                console.log(person);
                document.getElementById('usuario').value=userData.email;
                document.getElementById('email').value=userData.email;
                document.getElementById('nombre').value=userData.first_name;
                document.getElementById('apellido').value=userData.last_name;

                document.getElementById('holi').innerHTML=userData.first_name;
                $.ajax({
                  method:"POST",
                  url:"login2",
                  data: person,
                  dataType: 'text',
                  success: function (data){
                    console.log("HOLI");
                    if (data=="ok"){
                        console.log("HOLI2");
                    }
                  }
                });
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
