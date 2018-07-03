// main js file for kerberus

// slow scroll to anchor
$(document).ready(function(){
  // Add smooth scrolling to all links
  $("a").on('click', function(event) {

    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {

        if (this.hash === "#about-section") {
            setAbout();
        }

        if (this.hash === "#services-section") {
            setServices();
        }

        if (this.hash === "#contact-section") {
            setContact();
        }

        if (this.hash === "#top") {
            setHome();
        }

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
              document.location.href = String( document.location.href ).replace( "/#", "" );
          }
      });
    } // End if
  });
});

$(window).on("scroll", function() {
  var scrollPosition = scrollY || pageYOffset;

  if (scrollPosition < $("#about-section").position().top - 50) { //} - $(window).height()) {
      setHome()
  }

  if (scrollPosition > $("#about-section").position().top - 50 && // - $(window).height() - 3 &&
      scrollPosition < $("#services-section").position().top) { // - $(window).height() + 3) {
      setAbout()
  }

  if (scrollPosition > $("#services-section").position().top - 50 && //- $(window).height() - 3 &&
      scrollPosition < $("#services-section").position().top + 200) { // - $(window).height() + 3) {
      setServices()
  }

  // if (scrollPosition > $("#contact-link").position().top - $(window).height() - 3 &&
  //     scrollPosition < $("#contact-link").position().top - $(window).height() + 3) {

    if (scrollPosition === $(document).height() - $(window).height()) {
      setContact()
  }

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

