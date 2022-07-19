var minimized = false
var maximized = false



$(document).ready(function(){
  new_rooms()

  $("#table1").css("display", "none")
  $("#table2").css("display", "none")

})
function rooms_r(){
        $.ajax({
            type: 'GET',
            url : "/room_request",
            success: function(response){

                $("#rooms").empty();
                $("#number_notifications").empty();

                for (var key in response.requests){
                  var temp="<div class='p_new'><h4> New Message: "+response.requests[key].msg_from+"</h4> <p>You have "+response.requests[key].new_msgs+" new messages from: "+response.requests[key].msg_from+"</p><div id='add_style_button'> <button style='float:none' id='b_notification' type='submit' onclick=msg_user("+response.requests[key].request_to +","+ response.requests[key].request_from +")><span class='material-icons md-18'>chat</span></button></div></div>";


                  $("#rooms").append(temp);
                }
                if (response.requests.length > 0){
                  $("#number_notifications").append("("+response.requests.length + ")")
                  document.title = "MSA Menu ("+response.requests.length + ")"
                }
            },
        });
    }

var nr_time = setInterval(new_rooms, 10000)

function new_rooms(){
    $.ajax({
        type: 'GET',
        url : "/check/room",
        success: function(response){
            if (response.new_requests == "yes"){
              rooms_r()
              }

            else if (response.new_requests != "yes" && $(".p_new").length > 0){
              $("#rooms").empty();
              $("#number_notifications").empty();
              document.title = "MSA Menu"
              }
            }
        })
};


function msg_user(id1, id2){
  if ($(".chat_div").length == 1){
    $("#msg").html("You can only have 1 simultaneous chat tabs")
  }
  else {

    minimized = false

    $("#m_not").html("")
    document.title = "MSA Menu"
    $("#number_notifications").empty();


    $("#msg").html("")
    const div = document.createElement("div") // create and set element to be used
    div.setAttribute("id", "chat_div") // on the chat page javascript.
    div.setAttribute("class", "chat_div")

    $("button[name="+id2+"]").attr("disabled", true) // disable the button.

    $.ajax({
      type: 'GET',
      url: '/chat/' + id1 +'/' + id2,
      success: function(response){
        div.innerHTML = response
        $(".chat").append(div)

      }
    })
  }
}

function add_user(user2_id){
  $("#"+user2_id).remove()
  $.ajax({
    type: 'POST',
    url: '/msa/friend',
    data:{
      user2_id:user2_id,
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      action:"add_friend",
    }
  });
  $("#all_tables").load(window.location.href + " #all_tables")

}


function unfriend_user(friend_id){
  $("#"+friend_id).remove()

  $.ajax({
    type: 'POST',
    url: '/msa/friend',
    data:{
      friend_id:friend_id,
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      action:"unfriend",
    }
  });
    $("#all_tables").load(window.location.href + " #all_tables")
}

$(document).on('submit','#search_form',function(e){
  e.preventDefault();

  var id1 = $("#id1").val()
  var id2 = $("#id2").val()

  msg_user(id1, id2)

})



function minimize(element){

  if (maximized){
    $(".chat_maximized").attr("class", "chat_div")
    $(".style_content").css("max-height", "400px")
    $(".chat").css("max-height", "80%")

    maximized = false
  }
  else {
    $("#"+element).css("height", "30px")
    $("#"+element).css("overflow", "hidden")

    minimized = true
  }
}

function maximize(element){
  $("#"+element).css("height", "auto")
  $("#"+element).css("overflow", "auto")

  if (!minimized && ($('body').width() > 1000)){
    $(".chat_div").attr("class", "chat_maximized")

    maximized = true
  }

  minimized = false

  $("#m_not").html("")
  document.title = "MSA Menu"


}

function collapse_element(element){
  if ($("#alert_div").length > 0){
    $("#alert_div").remove()
  }

  if ($("#" + element).css("display") == "none"){
    $("#" + element).css("display", "table")


  }
  else{
    $("#" + element).css("display", "none")

  }

}


if ($('body').width() < 1000){
    $("#userlist").css("width", "35%")

    $("#friendlist").css("width", "35%")
}

if ($('body').width() < 768){
  $("#userlist").css("width", "45%")
  $("#userlist").css("font-size", "12px")

  $("#friendlist").css("width", "45%")
  $("#friendlist").css("font-size", "12px")

}
