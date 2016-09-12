define([
    'jquery',
    'bootstrap',
],

function ($) {
	$('.detail-launch').click(function(e){
		$.ajax({
			type: "GET",
            url: $(this).data("showurl"),
            success: function(res) {
				$('#show_detail_modal').html(res).modal();
            }
        });
	});
	//function initMap(ltlng) {
	//	console.log('initmap')
	//	var thisltlng = new google.maps.LatLng(ltlng.split(",")[0], ltlng.split(",")[1]);
	//	var mapOptions = {
	//		zoom: 12,
	//		center: thisltlng,
	//		mapTypeId: google.maps.MapTypeId.ROADMAP
	//	};
	//	var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
	//	console.log('map')
	//	console.log(map)
	//	var marker = new google.maps.Marker({
	//		position: thisltlng,
	//		map: map,
	//	});
	//	console.log('marker')
	//	console.log(marker)
	//	return map;
	//}
	//$('#show_detail_modal').on('shown.bs.modal', function(){
	//	console.log('show modal')
	//	var ltlng = $(this).find('#venue_address').val();
	//	console.log(ltlng)
	//	var modalMap = initMap(ltlng);
	//	console.log('modalMap')
	//	console.log(modalMap)
	//	google.maps.event.trigger(modalMap, "resize");
	//	console.log('reszied')
	//});
});