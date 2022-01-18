
$(document).ready(function (){
  $("#s_pass").on("click", function(){
    var p1 = $("#password1")
    var p2 = $("#password2")
    var old_p = $("#old_password")

    if (p1.attr("type") == "password"){
      p1.attr("type", "text")
      p2.attr("type", "text")
      old_p.attr("type", "text")

    }
    else {
      p1.attr("type", "password")
      p2.attr("type", "password")
      old_p.attr("type", "password")


    }
  })
})



function refresh_feedback(){
  $(".form-control").each(function(){
    $(this).removeClass("is-invalid")
    $(this).addClass("is-valid")
  })
}

function validate_user(un, e){
  if (un.val().length < 4 || un.val().length > 32){
    e.preventDefault();
    un.addClass("is-invalid")
    $("#feedback-username").html("Usernames must have more than 4 characteres and less than 32!")

  }
}

function validate_email(em, e){
     var emailReg = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;

     var result = emailReg.test(em.val());

    if ( !result){
      e.preventDefault();
      em.addClass("is-invalid")
      $("#feedback-email").html("Invalid email!")
    }

}

function validate_password(p1,e) {

  if (p1.val().length < 6 || p1.val().length > 64){
    e.preventDefault();
    p1.addClass("is-invalid")
    $("#feedback-pass1").html("Passwords must have more than 6 characteres and less than 64!")

  }

  if ($.isNumeric(p1.val()) ) {
    e.preventDefault();
    p1.addClass("is-invalid")
    $("#feedback-pass1").html("Passwords must have at least a letter!")

  }
}

function validate_password2(p1,p2,e){
  if (p1.val() != p2.val()){
    e.preventDefault();
    p2.addClass("is-invalid")
    $("#feedback-pass2").html("Passwords don't match!")
  }
}

function register_validation(un,em,p1,p2,e){
  refresh_feedback()
  validate_user(un,e)
  validate_email(em,e)
  validate_password(p1,e)
  validate_password2(p1,p2, e)
}

function login_validation(un,p1, e){
  refresh_feedback()
  validate_user(un,e)
  validate_password(p1, e)


  if ($("#g-recaptcha-response").val() === ""){
    e.preventDefault();
    $("#feedback-captcha").html("Captcha required!")

  }

}

function pchange_validation(p1,p2, old_p,e){
  refresh_feedback()
  validate_password(p1,e)
  validate_password2(p1,p2, e)

  if (old_p.val() === "" || old_p.val().length < 6){
    e.preventDefault();
    old_p.addClass("is-invalid")
    $("#old_p_feedback").html("Please input a valid password!")

  }
}
