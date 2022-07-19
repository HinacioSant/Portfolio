$(document).on('submit', '#ResetForm', function(e){
  var p1 = $("#password1")
  var p2 = $("#password2")


  refresh_feedback()
  validate_password(p1,e)
  validate_password2(p1,p2,e)

});
