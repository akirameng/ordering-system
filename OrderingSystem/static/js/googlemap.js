var map;
var MY_MAPTYPE_ID = 'custom_style';
var icon = 'https://imageshack.com/i/ipuGViCSp';
var myIcon = 'https://imageshack.com/i/hlaoqEdZp';


function initialize() {
    var featureOpts = [
   {
       "featureType": "landscape",
       "stylers": [
           {
               "hue": "#FFBB00"
           },
           {
               "saturation": 43.400000000000006
           },
           {
               "lightness": 37.599999999999994
           },
           {
               "gamma": 1
           }
       ]
   },
   {
       "featureType": "road.highway",
       "stylers": [
           {
               "hue": "#FFC200"
           },
           {
               "saturation": -61.8
           },
           {
               "lightness": 45.599999999999994
           },
           {
               "gamma": 1
           }
       ]
   },
   {
       "featureType": "road.arterial",
       "stylers": [
           {
               "hue": "#FF0300"
           },
           {
               "saturation": -100
           },
           {
               "lightness": 51.19999999999999
           },
           {
               "gamma": 1
           }
       ]
   },
   {
       "featureType": "road.local",
       "stylers": [
           {
               "hue": "#FF0300"
           },
           {
               "saturation": -100
           },
           {
               "lightness": 52
           },
           {
               "gamma": 1
           }
       ]
   },
   {
       "featureType": "water",
       "stylers": [
           {
               "hue": "#0078FF"
           },
           {
               "saturation": -13.200000000000003
           },
           {
               "lightness": 2.4000000000000057
           },
           {
               "gamma": 1
           }
       ]
   },
   {
       "featureType": "poi",
       "stylers": [
           {
               "hue": "#00FF6A"
           },
           {
               "saturation": -1.0989010989011234
           },
           {
               "lightness": 11.200000000000017
           },
           {
               "gamma": 1
           }
       ]
   }];


    var mapCanvas = document.getElementById('map-canvas');

    var mapOptions = {

        scaleControl: true,
        mapTypeControl: false,
        streetViewControl: false,
        zoomControl: true,
        zoomControlOptions: {
            position: google.maps.ControlPosition.RIGHT_BOTTOM
        },
        center: new google.maps.LatLng(49.2503, -123.0500),
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP,

        mapTypeId: MY_MAPTYPE_ID
    };

    map = new google.maps.Map(mapCanvas, mapOptions);

    //get address from users
    if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = new google.maps.LatLng(position.coords.latitude,
                                      position.coords.longitude);



            map.setCenter(pos);
            var marker = new google.maps.Marker({
                map: map,
                position: pos,
                icon: myIcon

            });
        }, function() {
            handleNoGeolocation(true);
        });
    } else {
   // Browser doesn't support Geolocation
        handleNoGeolocation(false);
    }

       //customize the map
    var styledMapOptions = {
        name: 'Custom Style'
    };

    var customMapType = new google.maps.StyledMapType(featureOpts, styledMapOptions);

    map.mapTypes.set(MY_MAPTYPE_ID, customMapType);



    setMarkers(map,restaurants);

}

     //set markers on restaurants' addresses
function setMarkers(map, location){
    for (var i = 0; i < restaurants.length; i++){
        var restaurant = restaurants[i];
        var myLatLng = new google.maps.LatLng(restaurant[1], restaurant[2]);

        var marker = new google.maps.Marker({
            map: map,
            animation: google.maps.Animation.DROP,
            position: myLatLng,
            icon: icon,
            url: restaurant[6]

        });

        var content = '<div>' + '<h5><a href=\"'+restaurant[6]+'\">'
                 + restaurant[0]+ '</a></h5>'
                 + '<div class="secondary round label small-centered rate_label">'+ restaurant[5]
                 + '</div>'+'<div class="info round label small-centered rate_label">'+ restaurant[4] + '</div>' + '</div>';


        var infowindow = new google.maps.InfoWindow();
        google.maps.event.addListener(marker,'mousemove', (function(marker,content,infowindow){
            return function() {
                infowindow.setContent(content);
                infowindow.open(map,marker);
            };
        })(marker,content,infowindow));

        google.maps.event.addListener(marker, 'click', function() {
            window.location.href = this.url;
        });


        google.maps.event.addListener(marker,'mouseout', (function(marker,content,infowindow){
            return function() {
                infowindow.close();
            };
        })(marker,content,infowindow));

    }

}



