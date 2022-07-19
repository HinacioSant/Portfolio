

$(document).on('submit', '#ChangeForm', function(e){

  var password1 = $("#password1")
  var password2 = $("#password2")
  var old_p = $("#old_password")


  pchange_validation(password1,password2, old_p, e)

});
