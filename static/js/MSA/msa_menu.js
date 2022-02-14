$(document).ready(function(){
  rooms_r()

})
function rooms_r(){
        $.ajax({
            type: 'GET',
            url : "/room_request",
            success: function(response){

                $("#rooms").empty();
                for (var key in response.requests)
                {
                  var temp="<a href=/chat/"+response.requests[key].request_from+"/"+response.requests[key].request_to+">Room:"+response.requests[key].room+"</a> <button type='submit' id="+response.requests[key].request_from+" onclick=msg_user("+response.requests[key].request_to +","+ response.requests[key].request_from +")><span class='material-icons md-18'>chat</span></button>";

                    $("#rooms").append(temp);
                }
            },
        });
    }

var nr_time = setInterval(new_rooms, 4000)

function new_rooms(){
    $.ajax({
        type: 'GET',
        url : "/check/room",
        success: function(response){

            if (response.new_requests == "yes" && $("#"+response.room).length == 0){
              rooms_r()
            }
            }
        })
};


function msg_user(id1, id2){
  if ($(".chat_div").length == 1){
    $("#msg").html("You can only have 1 simultaneous chat tabs")
  }
  else {

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
    url: '/msa/menu/',
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
    url: '/msa/menu/',
    data:{
      friend_id:friend_id,
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      action:"unfriend",
    }
  });
    $("#all_tables").load(window.location.href + " #all_tables")
}


function minimize(element){
  $("#"+element).css("height", "35px")
  $("#"+element).css("overflow", "hidden")



}

function maximize(element){
  $("#"+element).css("height", "auto")
  $("#"+element).css("overflow", "auto")


}
