
$(document).ready(function(){
  // mobile navigation - fade animation for menu
  $('#toggle').click(function() {
    $('#rel').fadeToggle('slow');
    });
  $('.fa-times').click(function() {
      $('#rel').fadeToggle('slow');
    });

  // begin on scroll stuff for header - change colours if need be!
  var scroll_start = 0;
  var startchange = $('.pos-fixed');
  var offset = startchange.offset();
  $(document).scroll(function() {
    scroll_start = $(this).scrollTop();
    if (scroll_start > offset.top ) {
      $('.pos-fixed').css('background-color', '#00a8ff');
      $('.pos-fixed').css('box-shadow', '0px 2px 10px rgba(0,0,0,0.3)');
      $('.logo').css('color', 'white');
      $('#toggle').css('color', 'white');
      $('a').addClass('scrolled');
      $('span').removeClass('blue');

      }
    else {
      $('.pos-fixed').css('background-color', 'white');
      $('.pos-fixed').css('box-shadow', '0px 0px 0px #fff');
      $('#blue').css('color', '#00a8ff');
      $('#toggle').css('color', '#00a8ff');
      $('a').removeClass('scrolled');
      // fixes weird on hover action when scrolled is added.
      $('span').addClass('blue');
      }
      // end of if / else statment above

  });
    // scroll to portfolio section
    $('.port').click(function() {
    $('html, body').animate({
      scrollTop: $('.portfolio').offset().top
    },1200)
  });
  // see our work button animates to portfolio section
  $('.scroll-port').click(function() {
    $('html, body').animate({
      scrollTop: $('.portfolio').offset().top
    }, 1200)
  });
  // scroll for about page. When the button is clicked, it will animate to a specific section, by id or class.
  $('.team-scroll').click(function() {
    $('html, body').animate({
      scrollTop: $('.team-profiles').offset().top
    }, 1200)
  });

  });





//end of document ready






// on scroll until top of services div, change logo and navigation color to white and background of pos-fixed to #00a8ff
