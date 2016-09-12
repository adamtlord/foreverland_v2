define([
    'jquery',
    'bootstrap',
    'magnific-popup',
    'instafeed',
],

function ($) {
    $(function(){
        var feed = new Instafeed({
            clientId: 'b1b89352013d4bc58352ff847c69c3c3',
            get: 'user',
            userId: 201585387,
            accessToken: '201585387.b1b8935.09b707305b2b4cf3a7e68aab25a66dff',
            resolution: 'standard_resolution',
            template: '<a href="{{image}}" class="thumb" title="{{caption}}"><img src="{{image}}"" /></a>',
            after: function(){
                $('#instafeed_spinner').fadeOut('fast');
            }
        });
        feed.run();

		$('.album-popup').magnificPopup({
			delegate: 'a',
			type:'image',
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