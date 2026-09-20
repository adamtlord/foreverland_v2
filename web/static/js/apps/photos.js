import '../lib/magnific-popup.min.js';

const $ = window.jQuery;

$(function() {
  $('.album-popup').magnificPopup({
    delegate: 'a',
    type: 'image',
    gallery: {
      enabled: true
    },
    zoom: {
      enabled: true,
      duration: 300,
      easing: 'ease-in-out',
      opener: function(openerElement) {
        return openerElement.is('img') ? openerElement : openerElement.find('img');
      }
    },
    image: {
      titleSrc: 'title'
    }
  });
});
