
$(document).on('submit', '#RegisterForm', function(e){
  // Validation check
  var username = $("#username")
  var email = $("#email")
  var password1 = $("#password1")
  var password2 = $("#password2")

  register_validation(username,email,password1,password2, e)
});
