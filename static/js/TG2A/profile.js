function delete_img(image_id){
  if (confirm('Are you sure you want to delete this image?')) {

    var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
    $.ajax({
      type: 'POST',
      url: '/TG2A/add',
      data:{
        csrfmiddlewaretoken:csrf_token,
        image_id:image_id,
        action:"delete_img",
      },
    })

    const refresh_time = setTimeout(refresh_tables, 500)

    function refresh_tables() {
      $("#all_tables").load(window.location.href + " #all_tables")
    }


  }
  else {
    console.log('OK!');
}


}


function delete_fav(fav_id){
  if (confirm('Are you sure you want to unfavorite this image?')) {

    var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
    $.ajax({
      type: 'POST',
      url: '/gallery/'+ fav_id,
      data:{
        csrfmiddlewaretoken:csrf_token,
        fav:"favorite_border",
      },
    })

    const refresh_time = setTimeout(refresh_tables, 500)

    function refresh_tables() {
      $("#all_tables").load(window.location.href + " #all_tables")
    }


  }
  else {
    console.log('OK!');
}


}


scrollContainer.addEventListener("wheel", (evt) => {
    evt.preventDefault();
    scrollContainer.scrollLeft += evt.deltaY;
});
