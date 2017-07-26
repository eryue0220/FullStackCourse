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

    function ViewModel(map) {
        var self = this;

        self.query = ko.observable();
        self.currentDirection = ko.observable();
        self.mapList = ko.observableArray([]);

        initialList.map(function(item, index) {
            var marker = setMarkerAndInfoWindow(item, map);
            item.index = index;
            item.marker = marker;
            self.mapList.push(item);
        });

        self.filterPosition = ko.computed(function() {
            if (!self.query()) {
                self.mapList().forEach(function(lcoation) {
                    lcoation.marker.setVisible(true);
                });
                return self.mapList();
            }

            self.mapList().forEach(function(location) {
                var matched = location.title.toLowerCase().indexOf(self.query().toLowerCase()) !== -1;
                location.marker.setVisible(matched);
            });

            return ko.utils.arrayFilter(self.mapList(), function(map) {
                return map.title.toLowerCase().indexOf(self.query()) > -1;
            });
        });

        self.filter = function(ko, e) {
            self.query(e.target.value.toLowerCase());
        };

        self.slide = function(ko, e) {
            self.currentDirection(e.target.className.baseVal === 'arrow-left' ? 'left' : 'right');
        };

        self.animation = ko.computed(function() {
            return self.currentDirection() === 'left' ? 'slide-left' : 'slide-right';
        });

        self.setPos = function(ko, e) {
            google.maps.event.trigger(ko.marker, 'click');
        };
    };

    return ViewModel;
})();

function openInfoWindow(marker, infowindow) {
    infowindow.setContent('');
    infowindow.marker = marker;
    infowindow.addListener('closeclick', function() {
        infowindow.marker = null;
    });

    getLocalNews(infowindow, marker, map);
}

function getLocalNews(infowindow, marker, map) {
    $.ajax({
            url: 'https://api.nytimes.com/svc/search/v2/articlesearch.json',
            method: 'GET',
            data: {
                'api-key': 'cc1dfcf434454ef4b221282aa563f6ad',
                query: marker.title
            }
        })
        .done(function(res) {
            if (res && res.status === 'OK') {

                var docs = res.response.docs[0] || {},
                    content = (
                        '<div>' +
                        '<h3>' + marker.title + '</h3>' +
                        '<div>' +
                        '<a target="_blank" href="' + docs.web_url + '">' +
                        docs.headline.main +
                        '</a>' +
                        '</div>' +
                        '</div'
                    );

                infowindow.setContent('<div>' + content + '</div>');
                infowindow.open(map, marker);
            }
        })
        .fail(function(err) {
            infowindow.setContent(
                '<div>' +
                '<h3>' + marker.title + '</h3>' +
                '<p>Service Error</p>' +
                '</div>'
            );
            infowindow.open(map, marker);
        });
}

function setMarkerAndInfoWindow(item, map) {
    var self = this;
    var maps = google.maps;
    var timer = null;
    var marker = new maps.Marker({
        title: item.title,
        position: item.position,
        animation: maps.Animation.DROP,
        map: map
    });

    var infoWindow = new maps.InfoWindow({
        content: 'Lat:' + item.position.lat + ', ' + 'Lng: ' + item.position.lng
    });

    marker.addListener('click', function() {
        marker.setAnimation(maps.Animation.BOUNCE);
        openInfoWindow(this, infoWindow);

        if (timer) clearTimeout(timer);
        timer = setTimeout(function() {
            marker.setAnimation(null);
        }, 2000);
    });

    return marker;
}

function initMap() {
    var NYC = {
        lat: 40.7413549,
        lng: -73.99802439999996
    };
    var mapArray = [];
    var map = new google.maps.Map(document.getElementById('map'), {
        center: NYC,
        zoom: 18
    });

    ko.applyBindings(new mapping(map));
}


// handle loading google map error
function handleMapError(err) {
    console.log('err', err);
}