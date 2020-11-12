define([
    'jquery',
    'underscore',
    'bootstrap'
],

function ($) {
    $('html').addClass('js-ready');
    $('#navbar_toggle').click(function(e){
        e.preventDefault();
        $('html').toggleClass('js-nav');
    });
    $('#nav_close_btn').click(function(e){
        e.preventDefault();
        $('html').removeClass('js-nav');
    });
    ! function (d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0],
            p = /^http:/.test(d.location) ? 'http' : 'https';
        if (!d.getElementById(id)) {
            js = d.createElement(s);
            js.id = id;
            js.src = p + "://platform.twitter.com/widgets.js";
            fjs.parentNode.insertBefore(js, fjs);
        }
    }(document, "script", "twitter-wjs");
});