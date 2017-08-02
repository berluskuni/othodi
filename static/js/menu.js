$(document).ready(function() {
    var mql = window.matchMedia('all and (max-width: 992px)');
    if (mql.matches) {
        $('#sandwich').show();
        $('.menu-container').hide('fast');
        $('.content-container').removeClass('content-padding');

    } else {
        $('#sandwich').hide();
        $('.content-container').addClass('content-padding');
        $('.menu-container').show('fast');
    }

    var list = $(".menu-list a");
    for (i = 0 ;i<list.length;i++){
        if (list[i].href==location.href){
            list.eq(i).children().addClass('active-menu-element');
        }

    }
});

$('#sandwich').click(function () {
    if ($('.menu-container').is(":visible"))
    {
        $('.menu-container').hide('fast');
        $('.content-container').removeClass('content-padding');

    }
    else{
        $('.menu-container').show('fast');
        $('.content-container').addClass('content-padding');
    }
});

$( window ).resize(function() {
    var mql = window.matchMedia('all and (max-width: 992px)');
    if (mql.matches) {
        $('#sandwich').show();
        $('.menu-container').hide('fast');
        $('.content-container').removeClass('content-padding');

    } else {
        $('#sandwich').hide();
        $('.content-container').addClass('content-padding');
        $('.menu-container').show('fast');
    }

    var list = $(".menu-list a");
    for (i = 0 ;i<list.length;i++){
        if (list[i].href==location.href){
            list.eq(i).children().addClass('active-menu-element');
        }

    }
});