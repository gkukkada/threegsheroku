var latlng = new google.maps.LatLng(42.745334, 12.738430);

function addmarker(latilongi) {
    var marker = new google.maps.Marker({
        position: latilongi,
        title: 'new marker',
        draggable: true,
        map: map
    });
    map.setCenter(marker.getPosition())
}
