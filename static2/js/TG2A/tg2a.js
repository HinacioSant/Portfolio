$(document).ready(function(){ // Format to different display sizes.
  if ($('body').width() < 1000){
      $(".gallery_content").css("width", "50%")
}
  if ($('body').width() < 700){
      $(".gallery_content").css("width", "100%")
  }

});


var waypoint = new Waypoint({ // Waypoint function
  element: document.getElementById("next_page_num"), // Element waypoint
  handler: function(direction) {
    var num = this.element.innerHTML // On scroll this element innerHTML will get the value of the next page.
    if (num === ''){ // If the value is ''(default)
      next_page(1) // It just call the page 1.
    }
    else {  // Else it call the next page.
      next_page(num)
    }




  },
  offset: 'bottom-in-view'

});


function add_form() { // Set the visuals of add form.
  if ($(".background_add").is(":hidden")){
    $(".background_add").show()

    $("#page_content").addClass("blur") // Blur class presented on the css
  }


  else {
    $(".background_add").hide()
    

    $("#page_content").removeClass("blur")

}
};




function next_page(num){ // Infinite scroll function. num variable is presented by the waypoint.
    $.ajax({

    type: 'GET',
    url : "/gallery_items/"+ num,
    success: function(response){

      for (var key in response.items){
        var temp ="<div> <a id='image_link' href='gallery/"+ response.items[key].id +"'><img id='images' class='rounded d-block' src="
                   + response.items[key].thumbnail_url +"></a></div>"

      // turn this into a function later

        var a = $("#column-1 a").length
        var b = $("#column-2 a").length
        var c = $("#column-3 a").length


        if ($('body').width() > 1000){ // Elements will be appended by display size.

          if (a == b && a == c) { // Each column will get a image until not image remains.
            $("#column-1").append(temp)
          }
          if (b < a) {
            $("#column-2").append(temp)
          }
          if (c < b){
            $("#column-3").append(temp)
          }
        }

        else {
          if (a == b) {
            $("#column-1").append(temp)
          }
          if (b < a) {
            $("#column-2").append(temp)
          }
        }


    }

    if (response.page === ''){ // If the response comes back as '', there no more pages.
      waypoint.disable() // disable waypoint
      $("#next_page_num").html("No more content to load!")
    }
    else { // Else add to the waypoint element the value
      $("#next_page_num").html(response.page)
      Waypoint.refreshAll() // And refresh the waypoint.

    }
  }
})
};
