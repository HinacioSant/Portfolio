$("#f_button").on("click", function() {
  if( $('#fav_id').html() === "favorite_border"){ // Change the icon on click.
    $('#fav_id').html("favorite")
  }
  else {
    $('#fav_id').html("favorite_border")
  }

})

$(document).on('submit','#fav_form',function(e){ // Submit the form.

  var img_id = $("#image_id").html()
  e.preventDefault();

        $.ajax({
            type: 'POST',
            url: '/gallery/'+ img_id,
            data: {
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    fav:$('.material-icons').html(),
                  }
        });


    });


function report_form(){
  if ($(".background_add").is(":hidden")){
    $(".background_add").show()
  }

  else {
    $(".background_add").hide()
  }

}


$(document).on('submit','#report_form',function(e){ // Submit the form.
  var img_id = $("#image_id").html()

  e.preventDefault();

        $.ajax({
            type: 'POST',
            url: '/report',
            data: {
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    img_id:img_id,
                    reason:$('#reason').val(),
                    m_info:$('#m_info').val(),
                  }
        });
        $('#reason').val("")
        $('#m_info').val("")
        report_form()

    });
