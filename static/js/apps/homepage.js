define([
    'jquery',
    'underscore',
    'bootstrap',
    'jquery.flexslider',
],

function ($) {
    var w = $(window);
    var nvo = 0;
    function setHeights(){
        // var v = $('#video_wrap iframe');
        // var vh = Math.floor(0.5625 * v.width());
        var ch = $('#bio .carousel').height();
        var bt = $('#bio section');
        var bth = bt.height();
        // v.css('min-height', vh + 'px');
        if(w.width() > 992){
            bt.css('height', ch + 'px');
        }else {
            bt.css('height', 'auto');
        }
        nvo = $('#home_nav').offset().top;
    }
    function setFixed(){
        $('#next_show').toggleClass('up', $(this).scrollTop() > (nvo - 40));
        $('#home_nav, #nav_push').toggleClass('up', $(this).scrollTop() > nvo);
    }
    $(function() {
        // Hompage specific js goes here, if not already in a module
        $('.flexslider').flexslider({
            slideshowSpeed: 4000,
            randomize:true,
            controlNav: false,
            directionNav:false
        });
        setHeights();
        var resetHeights = _.debounce(setHeights, 300);
        var resetFixed = _.throttle(setFixed, 100);
        $(w).resize(resetHeights);
        $(w).scroll(resetFixed);
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