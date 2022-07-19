var maximized_n = false

/* Set the width of the side navigation to 230px and the left margin of the page content to 230px */
function openNav() {
  if (document.getElementById("mySidenav").style.width > "100px") {
    closeNav()
  }
  else {
    if ($('body').width() < 1000){
      document.getElementById("mySidenav").style.width = "160px";
      document.getElementById("n_div").style.marginLeft = "160px";
      document.getElementById("mySidenav").style.borderRight = "1px solid gray";

    }
    else {
      document.getElementById("mySidenav").style.width = "230px";
      document.getElementById("n_div").style.marginLeft = "230px";
      document.getElementById("mySidenav").style.borderRight = "1px solid gray";
    }




  };
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("n_div").style.marginLeft = "0";
  document.getElementById("mySidenav").style.borderRight = "";




}

// On click of the add button will show/hide the add bullet div.
function Add_toggle(element){
  if ($("." + element).css("display") == "none"){
    $("." + element).show()
    localStorage.setItem(element, "show")
  }


  else {
    $("." + element).hide()
    localStorage.setItem(element, "hide")

  }

}

function remove_element(element){
  if (element == "note_edit_div"){
    $("." + element).remove()
  }

  else {
    $("." + element).css("display", "none")
    localStorage.setItem(element, "hide")
  }
}

function maximize(element){
  if (maximized_n == false){
    if ($('body').width() < 1000){
      $("textarea").attr("rows", "11");
    }
    else{
      $("textarea").attr("rows", "17");
    }

    $("." + element).css("width", "auto")
    $("." + element).css("height", "auto")
    $("." + element).css("top", "9%")
    $("textarea").css("resize", "vertical")
    maximized_n = true
    }

  else {
    $("textarea").attr("rows", "6");

    if ($('body').width() < 1000){
      $("." + element).css("width", "60%")
    }

    if ($('body').width() < 768){
      $("." + element).css("width", "80%")
    }

    else if ($('body').width() > 1000){
      $("." + element).css("width", "40%")
    }

    $("." + element).css("height", "auto")
    $("." + element).css("top", "20%")
    maximized_n = false
  }

}

function edit_note(note_id){
  $.ajax({
    type: 'GET',
    url: '/TDV/' + note_id +'/edit',
    success: function(response){
      $("#n_div").append(response)

    }
  })
}

// When changing tabs will remove the "show active" class from the previous tab.
var triggerTabList = [].slice.call(document.getElementsByName('notes'))
triggerTabList.forEach(function (triggerEl) {


  triggerEl.addEventListener('click', function (event) {
    $(triggerEl).removeClass("show active");
  })
});


// Local storage of the active tab.
$(document).ready(function(){
    $('[data-bs-toggle="tab"]').on('show.bs.tab', function(e) {
        localStorage.setItem('activeTab', $(e.target).attr('data-bs-target'));


    });


    // On first use the "activeTap" variable will be null so set home as active tab.
    var activeTab = localStorage.getItem('activeTab');
    // On delete will return undefined as the respective tab was deleted so set home as active tab.
    if ($(activeTab).attr("class") === undefined){
      $("#home").addClass("show active")
    }
    if(activeTab != null){
      $(activeTab).addClass("show active")
    }
    else {
      $("#home").addClass("show active")
    }

    // Local storage if the add bullet div was hidden or not.
    var add_v = localStorage.getItem('note_bullet_div');
    // Default is hidden.
    if (add_v === null){
      $(".note_bullet_div").hide()
    }


    if (add_v === "show") {
      $(".note_bullet_div").show()
    }

    else {
      $(".note_bullet_div").hide()

    }
});

if ($('body').width() < 1000){
  $(".material-icons").addClass("md-18")
}
