function count() {
    var catName = ['Catthy', 'Mice'];

    $.each($('.cat_name'), function(index, dom) {
        $(dom).text(catName[index]);
    });

    $('.cat').on('click', 'img', function() {
        var $num = $(this).next().find('.num');
        var count = parseInt($num.data('count'), 10);
        count += 1;
        $num.data('count', count).text(count);
    });
}

count();