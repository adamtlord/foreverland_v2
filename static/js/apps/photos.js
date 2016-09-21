define([
    'jquery',
    'bootstrap',
    'magnific-popup',
    'instafeed',
  ],

  function($) {
    $(function() {
      var feed = new Instafeed({
        clientId: 'e57e58115b304e319ef65ad52d8555ba',
        get: 'user',
        userId: 201585387,
        accessToken: '201585387.e57e581.dafbe9ceedf4475b909749652bbdb290',
        resolution: 'standard_resolution',
        template: '<a href="{{image}}" class="thumb" title="{{caption}}"><img src="{{image}}"" /></a>',
        after: function() {
          $('#instafeed_spinner').fadeOut('fast');
        }
      });
      feed.run();

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
  });