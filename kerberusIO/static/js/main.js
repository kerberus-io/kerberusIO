// main js file for kerberus

// slow scroll to anchor
$(document).ready(function(){
  // Add smooth scrolling to all links
  $("a").on('click', function(event) {

    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {

      // Prevent default anchor click behavior
      event.preventDefault();

      // Store hash
      var hash = this.hash;

      // Using jQuery's animate() method to add smooth page scroll
      // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
      $('html, body').animate({
        scrollTop: $(hash).offset().top - 45
      }, 800, function(){

        // Add hash (#) to URL when done scrolling (default click behavior)
          if (hash !== "#top") {
              window.location.hash = hash;
          } else {
              window.location.hash = "";
              // document.location.href = String( document.location.href ).replace( "/#", "" );
          }
      });
    } // End if
  });
});

// TODO: Set so scrolling (not clicking) decides what is active

$(window).on("scroll", function() {
  var scrollPosition = scrollY || pageYOffset;

  var id_array = getSectionIds();

  // alert(id_array);

  for (var i = 0, len = id_array.length; i < len; i++) {
      if ((i + 1) < len) {
          if (scrollPosition > $(id_array[i]).position().top - 50 &&
              scrollPosition < $(id_array[i + 1]).position().top) {
              removeActive(i - 1, id_array);
              setActiveSection(i, id_array);
          }
      } else {
          if (scrollPosition > $(id_array[i]).position().top - 50 &&
              scrollPosition < $(id_array[i]).position().top) {
              removeActive(i - 1, id_array);
              setActiveSection(i, id_array);
          }
      }
  }

  // if (scrollPosition < $("#about").position().top - 50) { //} - $(window).height()) {
  //     setHome()
  // }
  //
  // if (scrollPosition > $("#about").position().top - 50 && // - $(window).height() - 3 &&
  //     scrollPosition < $("#services").position().top) { // - $(window).height() + 3) {
  //     setAbout()
  // }
  //
  // if (scrollPosition > $("#services").position().top - 50 && //- $(window).height() - 3 &&
  //     scrollPosition < $("#contact").position().top) { // - $(window).height() + 3) {
  //     setServices()
  // }
  //
  // if (scrollPosition > $("#contact").position().top - 50 && //- $(window).height() - 3 &&
  //     scrollPosition < $("#contact").position().top) { // - $(window).height() + 3) {
  //     setContact()
  // }


  // if (scrollPosition === $(document).height() - $(window).height()) {
  //     setContact()
  // }

});

function setHome() {
    $( "#home-bullet" ).addClass( "active" );
    $( "#about-link" ).removeClass( "active" );
    $( "#services-link" ).removeClass( "active" );
    $( "#contact-link" ).removeClass( "active" );
}

function setAbout() {
    $( "#home-bullet" ).removeClass( "active" );
    $( "#services-link" ).removeClass( "active" );
    $( "#contact-link" ).removeClass( "active" );
    $( "#about-link" ).addClass( "active" );
}

function setServices() {
    $( "#home-bullet" ).removeClass( "active" );
    $( "#about-link" ).removeClass( "active" );
    $( "#contact-link" ).removeClass( "active" );
    $( "#services-link" ).addClass( "active" );
}

function setContact() {
    $( "#home-bullet" ).removeClass( "active" );
    $( "#about-link" ).removeClass( "active" );
    $( "#services-link" ).removeClass( "active" );
    $( "#contact-link" ).addClass( "active" );
}

function getSectionIds() {
    var ids = [];
    var elements = document.getElementsByClassName("id-anchor");
    for (var i = 0, len = elements.length; i < len; i++) {
        ids.push("#" + elements[i].id)
    }
    return ids;
}

function removeActive(i, arr) {
    for (var len = arr.length; i < len; i++) {

        var id = arr[i];

        if (i === 0) {
            id += "-bullet"
        } else {
            id += "-link"
        }

        $(id).removeClass('active');
    }
}


function setActiveSection(i, arr) {
    for (var j = 0; j < arr.length; j++) {

        if (i === j) {

            var id = arr[i];

            if (i === 0) {
                id += "-bullet"
            } else {
                id += "-link"
            }

            var anc = $(id);

            if (i === j) {
                anc.addClass('active');
            }
        }
    }
}


function submitActive() {
    $('form:visible').submit();

}
// select-nav

// $('#select-type').on('change', function (e) {
//   var $optionSelected = $("option:selected", this);
//   $("#select-type>option.active").removeClass("active");
//   $("#select-type>option.show").removeClass("show");
//   $optionSelected.tab('show')
// });

// $('.select-nav').on('change', function (e) {
//   var $optionSelected = $("option:selected", this);
//   $(".select-nav>option.active").removeClass("active");
//   $(".select-nav>option.show").removeClass("show");
//   $optionSelected.tab('show')
// });
//
// // Javascript to enable link to tab
// var url = document.location.toString();
// if (url.match('#')) {
//     $('.nav-tabs a[href="#' + url.split('#')[1] + '"]').tab('show');
// }
//
// // Change hash for page-reload
// $('.nav-tabs a').on('shown.bs.tab', function (e) {
//     window.location.hash = e.target.hash;
// });
