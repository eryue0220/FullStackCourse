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

    // YOUR CODE GOES HERE!

    return false;
};

$('#form-container').submit(loadData);