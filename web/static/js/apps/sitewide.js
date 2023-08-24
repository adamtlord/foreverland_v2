define(["jquery", "underscore", "bootstrap"], function ($) {
  $("html").addClass("js-ready");
  $("#navbar_toggle").click(function (e) {
    e.preventDefault();
    $("html").toggleClass("js-nav");
  });
  $("#nav_close_btn").click(function (e) {
    e.preventDefault();
    $("html").removeClass("js-nav");
  });
});
