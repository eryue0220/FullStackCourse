function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');
    var $stree = $('#street');
    var $city = $('#city');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // load streetview
    if ($stree.val() !== '' && $city.val() !== '') {
        var href = 'http://maps.googleapis.com/maps/api/streetview?size=600x300&location=' +
            $stree.val() + ',' + $city.val()
        $body.append('<img class="bgimg" src="' + href + '">');
    }

    $.getJSON('https://api.nytimes.com/svc/search/v2/articlesearch.json', {
        q: $city.val(),
        sort: 'newest',
        'api-key': 'cc1dfcf434454ef4b221282aa563f6ad'
    }, function(resp) {
        var docs;
        $nytHeaderElem.text('NY Times articles about: ' + $city.val());
        if (resp && resp.status.toLowerCase() === 'ok') {
            docs = resp.response && resp.response.docs;

            for (var i = 0, len = docs.length; i < len; i++) {
                $nytElem.append(
                    '<li class="article">' +
                    '<a href="' + docs[i].web_url + '">' + docs[i].headline.main + '</a>' +
                    '<p>' + docs[i].snippet + '</p>' +
                    '</li>'
                );
            }
        }
    }).error(function(err) {
        console.error(err);
    });

    // YOUR CODE GOES HERE!
    $.ajax({
        url: 'https://en.wiksssspedia.org/w/api.php',
        type: 'get',
        data: {
            action: 'opensearch',
            search: $city.val(),
            format: 'json'
        },
        dataType: 'jsonp',
        jsonp: 'callback',
        success: function(data) {
            var list = data[1],
                url;

            for (var i = 0, len = list.length; i < len; i++) {
                url = 'https://en.wikipedia.org/wiki/' + list[i];
                $wikiElem.append(
                    '<li>' +
                    '<a href="' + url + '">' + list[i] + '</a>' +
                    '</li>'
                );
            }
        },
        error: function(err) {
            console.error(err);
        }
    });

    return false;
};

$('#form-container').submit(loadData);