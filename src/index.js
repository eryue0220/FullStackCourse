/**
 * @file src/index.js
 * @desc google map project
 * @author cinchen
 */

'use strict';

var initialList = [{
        title: '200 W, 18th, New York',
        position: {
            lat: 40.7413549,
            lng: -73.99802439999996
        }
    },
    {
        title: 'west elm',
        address: '112 W 18th St, New York, NY 10011',
        position: {
            lat: 40.7399988,
            lng: -73.9958785
        }
    },
    {
        title: 'Rubin Museum of Art',
        address: '150 W 17th St, New York, NY 10011',
        position: {
            lat: 40.7401773,
            lng: -73.9978141
        }
    },
    {
        title: 'Coppelia',
        address: '207 W 14th St, New York, NY 10011',
        position: {
            lat: 40.7389331,
            lng: -73.9999727
        }
    },
    {
        title: 'The Joyce Theater',
        address: '175 8th Ave, New York, NY 10011',
        position: {
            lat: 40.74277499999999,
            lng: -74.0005738
        }
    }
];

var mapping = (function() {
    function map(data) {
        this.title = ko.observable(data.title);
        this.description = ko.observable(data.description);
        this.address = ko.observable(data.address);
        this.index = ko.observable(data.index);
    }

    function ViewModel(mapMarkerArray) {
        var self = this;
        self.mapList = ko.observableArray([]);
        self.currentFilter = ko.observable();

        initialList.map(function(item, index) {
            item.index = index;
            self.mapList.push(item);
        });

        self.filterPosition = ko.computed(function() {
            if (!self.currentFilter()) return self.mapList();

            return ko.utils.arrayFilter(self.mapList(), function(map) {
                return map.title.toLowerCase().indexOf(self.currentFilter()) > -1;
            });
        });

        self.filter = function(ko, e) {
            self.currentFilter(e.target.value.toLowerCase());
        }
    };

    return ViewModel;
})();

function slide() {
    $('.icon').on('click', 'svg', function(e) {
        var $target = $(this);
        var $panel = $('.panel');
        var isRight = $target.hasClass('arrow-right');

        $panel.animate({
            left: isRight ? 0 : -410
        }, 500, function() {
            $('.arrow-' + (isRight ? 'right' : 'left')).css('display', 'none');
            $('.arrow-' + (!isRight ? 'right' : 'left')).css('display', 'block');
        });
    });
}

function openInfoWindow(marker, infowindow) {
    infowindow.setContent('');
    infowindow.marker = marker;
    infowindow.addListener('closeclick', function() {
        infowindow.marker = null;
    });
    infowindow.setContent('<div>' + marker.title + '</div>');
    infowindow.open(map, marker);
}

function setMarkerAndInfoWindow(item, map) {
    var self = this;
    var maps = google.maps;

    var marker = new maps.Marker({
        title: item.title,
        position: item.position,
        map: map
    });

    var infoWindow = new maps.InfoWindow({
        content: 'Lat:' + item.position.lat + ', ' + 'Lng: ' + item.position.lng
    });


    marker.addListener('click', function() {
        openInfoWindow(this, infoWindow);
    });

    return marker;
}

function initMap() {
    var uluru = {
        lat: 40.7413549,
        lng: -73.99802439999996
    };
    var mapArray = [];
    var map = new google.maps.Map(document.getElementById('map'), {
        center: uluru,
        zoom: 18
    });

    for (var i = 0, length = initialList.length; i < length; i++) {
        mapArray.push(setMarkerAndInfoWindow(initialList[i], map));
    }

    slide();
    ko.applyBindings(new mapping(mapArray));
}