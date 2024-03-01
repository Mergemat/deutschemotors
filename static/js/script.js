$(document).ready(function(){
    $('.slider').slick({
        arrows: false,
        slidesToShow: 1,
        infinite: true,
        autoplay: true,
        autoplaySpeed: 3000,
        centerMode: true,
        variableWidth: true,
    });
    $('.slider').on('wheel', (function(e) {
        e.preventDefault();
        if (e.originalEvent.deltaY < 0) {
          $(this).slick('slickNext');
        } 
        if (e.originalEvent.deltaY > 0) {
          $(this).slick('slickPrev');
        }
      }));
});