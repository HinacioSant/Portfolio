
function onSubmit(token) {
  document.getElementById("LoginForm").submit();
}

$(document).on('submit', '#LoginForm', function(e){
  var username = $("#username")
  var password1 = $("#password1")

  login_validation(username,password1, e)
});



if ($('body').width() < 770){
  $(".g-recaptcha").attr("data-size", "compact")
}
