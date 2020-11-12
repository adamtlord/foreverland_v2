define([
    'jquery',
    'jquery.scrollTo'
],

function ($) {
   if(document.location.hash=='#quotes'){
        $.scrollTo($('#testimonials'), 500, {easing:'swing', offset:-140} );
    }
});