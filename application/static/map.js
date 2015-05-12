// globals
var map;
var route_markers = [];
var activity_markers = [];
var activity_marker_index = 0;

// constants
var AUSTIN = new google.maps.LatLng(30.289748, -97.737843);
var METERS_TO_MILES = 0.000621371;

set_route_id="#set_route_button";
undo_id="#undo_button";
clear_markers_id="#clear_markers_button";

function update_route_buttons () {
    if (route_markers.length < 2) {
        $(set_route_id).prop('disabled',true);
    }
    else {
        $(set_route_id).prop('disabled',false);
    }
    if (route_markers.length < 1) {
        $(undo_id).prop('disabled',true);
        $(clear_markers_id).prop('disabled',true);
    }
    else {
        $(undo_id).prop('disabled',false);
        $(clear_markers_id).prop('disabled',false);
    }
}

function initialize ()
{
    var MAP_OPTIONS =
    {
        center: AUSTIN,
        zoom: 6,
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        mapTypeControl: true,
        mapTypeControlOptions:
        {
            style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
            position: google.maps.ControlPosition.LEFT_BOTTOM
        },
        panControl: true,
        panControlOptions:
        {
            position: google.maps.ControlPosition.LEFT_BOTTOM
        },
        zoomControl: true,
        zoomControlOptions:
        {
            style: google.maps.ZoomControlStyle.LARGE,
            position: google.maps.ControlPosition.LEFT_BOTTOM
        },
        scaleControl: true,
        streetViewControl: true,
        streetViewControlOptions:
        {
            position: google.maps.ControlPosition.LEFT_BOTTOM
        }
    };

    map = new google.maps.Map(document.getElementById('map-canvas'), MAP_OPTIONS);

    // This event listener will call addMarker() when the map is clicked.
    google.maps.event.addListener(map, 'click', function(event) {
        addMarker(event.latLng);
        });

    google.maps.event.addListener(map, 'center_changed', function() {
        var center = map.getCenter ();
        });

    google.maps.event.addListener(map, 'zoom_changed', function() {
        var zoom = map.getZoom ();
        });
}

function drawActivityMarkers (result, activities)
{
    var geo = google.maps.geometry.spherical;
    // display leg markers
    var legs = result.routes[0].legs;
    var index = 0;
    var total = 0;
    var last = legs[0].steps[0].path[0];
    var activity_total = 0;
    var path_total = 0;
    // reset gloabl markers
    activity_markers = [];
    for (var i=0; i<legs.length; i++)
    {
        var steps = legs[i].steps;
        for (var j=0; j<steps.length; j++)
        {
            var nextSegment = steps[j].path;
            for (var k=0; k<nextSegment.length; k++)
            {
                // get segment distance
                var pos = nextSegment[k];
                var segment_distance = geo.computeDistanceBetween (last, pos)
                // keep track of total path distance
                path_total += segment_distance;
                if (index < activities.length)
                {
                    var adist = activities[index].distance;
                    var miles = adist*METERS_TO_MILES;
                    // distance for this activity
                    total += segment_distance;
                    if (total > adist)
                    {
                        // add this marker position
                        activity_markers.push (pos);
                        //console.log('current activity distance = ' + miles);
                        //console.log('current path distance = ' + path_total*METERS_TO_MILES);
                        // keep track of total activity distance
                        activity_total += adist;
                        // you have to take into account the milage that you have gone over the marker
                        total = adist - total;
                        var marker = new google.maps.Marker({ position: pos, map: map, draggable:false, title:miles.toFixed(2).toString()+'m' });
                        marker.setIcon('http://maps.google.com/mapfiles/ms/icons/yellow-dot.png');
                        // compute the heading based upon last and current positions
                        // Headings are measured clockwise (90 degrees is true east).
                        var y = pos.lat () - last.lat ();
                        var x = pos.lng () - last.lng ();
                        var heading = Math.atan2 (y, x) * -180 / Math.PI + 90;
                        //console.log('current heading = ' + heading);
                        var sv_url = 'https://maps.googleapis.com/maps/api/streetview?size=400x400&location=' +
                            pos.lat().toString ()+','+pos.lng().toString ()+ '&fov=100&heading=' +
                            heading + '&pitch=0';
                        var s = 'Activity ' + (index + 1) + ', ' + miles.toFixed(2).toString () + ' miles' +
                            '<br>' +
                            '<a href="#" onclick="' +
                            'map.getStreetView().setPosition(new google.maps.LatLng(' +
                            pos.lat() + ',' + pos.lng() +
                            '));' +
                            'map.getStreetView().setPov({ heading: ' + heading.toString() + ', pitch: 0});' +
                            'map.getStreetView().setVisible(true);' +
                            'activity_marker_index = ' + index + ';' +
                            '">' +
                            '<br>' +
                            '<center>' +
                            '<button type="button">StreetView</button>' +
                            //'<img src="' + sv_url + '">' +
                            '</center>' +
                            '</a>';
                        attachInfoWindow (marker, s, map, pos);
                        // go to next activity
                        ++index;
                    }
                }
                // remember last position
                last = pos;
            }
        }
    }
    console.log('total activity distance = ' + activity_total*METERS_TO_MILES);
    console.log('total path distance = ' + path_total*METERS_TO_MILES);
    update_route_buttons ();
}

function enterStreetview ()
{
    console.log('activity markers length = ' + activity_markers.length);
    console.log('activity markers index = ' + activity_marker_index);
    var pos = activity_markers[activity_marker_index];
    var first;
    var second;
    if (activity_marker_index == 0)
    {
        first = activity_markers[0];
        second = activity_markers[1];
    }
    else
    {
        first = activity_markers[activity_marker_index - 1];
        second = activity_markers[activity_marker_index];
    }
    var y = second.lat () - first.lat ();
    var x = second.lng () - first.lng ();
    var heading = Math.atan2 (y, x) * -180 / Math.PI + 90;
    map.getStreetView().setPosition(new google.maps.LatLng(pos.lat(),pos.lng()));
    map.getStreetView().setPov({ heading: heading, pitch: 0});
    map.getStreetView().setVisible(true);
}

function previousStreetview ()
{
    if (activity_marker_index > 0)
        --activity_marker_index;
    enterStreetview ();
}

function nextStreetview ()
{
    if (activity_marker_index + 1 < activity_markers.length)
        ++activity_marker_index;
    enterStreetview ();
}

var animate_timeout;

function animateStreetview ()
{
    activity_marker_index = 0;

    var i = 0;
    for (i = 0; i < activity_markers.length; ++i)
    {
        animate_timeout = setTimeout(function() { nextStreetview(); }, 2000);
    }

    activity_marker_index = 0;
}

function stopAnimateStreetview ()
{
    clearTimeout (animate_timeout);
}

function leaveStreetview ()
{
    map.getStreetView().setVisible(false);
}

function drawRoute (route,activities)
{
    console.log('Route: ', route);
    console.log('route.length=' + route.length);
    if (!map)
        initialize ();
    console.log('Total activities ' + activities.length);
    var directionsDisplay = new google.maps.DirectionsRenderer();
    var directionsService = new google.maps.DirectionsService();
    if (route.length < 2)
        throw 'The route does not contain enough entries';
    // set start and end
    var START=new google.maps.LatLng (route[0]['lat'], route[0]['lng']);
    var END=new google.maps.LatLng (route[route.length-1]['lat'], route[route.length-1]['lng']);
    console.log('START= ' + START);
    console.log('END= ' + END);
    // set via points
    var waypts = [];
    for (var i = 1; i + 1 < route.length; i++) {
        waypts.push({ location: new google.maps.LatLng (route[i]['lat'], route[i]['lng']), stopover:false });
    }
    console.log('VIA= ' + waypts);
    directionsService.route(
        {
             origin: START,
             destination: END,
             waypoints: waypts,
             travelMode: google.maps.TravelMode.DRIVING
        }, function(result, status)
        {
            if (status == google.maps.DirectionsStatus.OK)
            {
                console.log('Got directions for specified route');

                // Show the directions on the map
                directionsDisplay.setDirections(result);
                directionsDisplay.setMap(map);

                drawActivityMarkers (result, activities);
            }
            else
                alert("Directions Request failed:" +status);
        });
}

function attachInfoWindow (marker, str, map, pos)
{
    // show a window containing mileage
    var infowindow = new google.maps.InfoWindow({
            content: str,
            map: map,
            position: pos
        });
    infowindow.close();
    google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map, marker);
    });
}

// Add a marker to the map and push to the array.
function addMarker(location) {
    if (route_markers.length == 1) {
        route_markers[route_markers.length - 1].setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png')
    }
    else if (route_markers.length != 0) {
        route_markers[route_markers.length - 1].setIcon('http://maps.google.com/mapfiles/ms/icons/yellow-dot.png')
    }
    var marker = new google.maps.Marker({ position: location, map: map, draggable:true });
    marker.setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png')
    route_markers.push(marker);
    update_route_buttons ();
}


// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
    for (var i = 0; i < route_markers.length; i++) {
        route_markers[i].setMap(null);
    }
    update_route_buttons ();
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    clearMarkers();
    route_markers = [];
    update_route_buttons ();
}


// Remove last marker
function undo() {
    if (route_markers.length != 0) {
        route_markers[route_markers.length - 1].setMap(null);
        route_markers.pop();
    }
    if (route_markers.length != 0) {
        route_markers[route_markers.length - 1].setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png')
    }
    update_route_buttons ();
}

function setRoute() {
    // convert to dict
    var m = []
    for (var i = 0; i < route_markers.length; i++) {
        m.push ({ 'lat' : route_markers[i].getPosition ().lat (), 'lng' : route_markers[i].getPosition ().lng ()});
    }
    // set it on the server
    $.getJSON($SCRIPT_ROOT + '/_set_route', { route_markers: JSON.stringify(m) });
    // reload the page so that the new route is shown
    location.reload ();
    update_route_buttons ();
}
