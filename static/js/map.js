ymaps.ready(init);
var myMap;

function init(){
    myMap = new ymaps.Map("map", {
        center: [55.76, 37.64],
        zoom: 7
    });
    resizeMap();
}

$(window).resize(function() {
    resizeMap();
});


function resizeMap() {
    var mqLg = window.matchMedia('all and (max-width: 1500px)');
    var mqMd = window.matchMedia('all and (max-width: 1405px)');
    var mqSm = window.matchMedia('all and (max-width: 1202px)');
    if (mqLg.matches) {
        $('#map').removeClass('bigMap');
        $('.map-container').removeClass('bigMap');
        $('#map').removeClass('mdMap');
        $('.map-container').removeClass('mdMap');
        $('#map').addClass('lgMap');
        $('.map-container').addClass('lgMap');
        myMap.container.fitToViewport();
    }
    if (mqMd.matches) {
        $('#map').removeClass('bigMap');
        $('.map-container').removeClass('bigMap');
        $('#map').removeClass('lgMap');
        $('.map-container').removeClass('lgMap');
        $('#map').addClass('mdMap');
        $('.map-container').addClass('mdMap');
        myMap.container.fitToViewport();
    }
    if(mqSm.matches){
        $('#map').removeClass('bigMap');
        $('.map-container').removeClass('bigMap');
        $('#map').removeClass('lgMap');
        $('.map-container').removeClass('lgMap');
        $('#map').removeClass('mdMap');
        $('.map-container').removeClass('mdMap');

        $('#map').removeClass('map-mobile');
        $('.map-container').removeClass('map-mobile');

        myMap.container.fitToViewport();
    }
    if (!mqLg.matches && !mqMd.matches){
        $('#map').removeClass('lgMap');
        $('.map-container').removeClass('lgMap');
        $('#map').removeClass('mdMap');
        $('.map-container').removeClass('mdMap');
        $('#map').addClass('bigMap');
        $('.map-container').addClass('bigMap');
        myMap.container.fitToViewport();
    }
}