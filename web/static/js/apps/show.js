define([
    'jquery',
    'bootstrap',
],

function ($) {
    $('[rel="tooltip"]').tooltip({
        placement: 'right',
        trigger: 'hover'
    });
});