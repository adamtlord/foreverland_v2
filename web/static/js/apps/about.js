import '../lib/jquery.scrollTo.js';

const $ = window.jQuery;

if (document.location.hash == '#quotes') {
    $.scrollTo($('#testimonials'), 500, {easing: 'swing', offset: -140});
}
