$(".left-button").click(function (e) {
    $(".left-button").addClass("active-button");
    $(".right-button").removeClass("active-button");
});
$(".right-button").click(function (e) {
    $(".right-button").addClass("active-button");
    $(".left-button").removeClass("active-button");
});

$('#quantity-button .order-button').click(function (e) {
    var buttonArray = $('#quantity-button .order-button');
    for (var i = 0 ; i <buttonArray.length;i++){
        $(buttonArray[i]).removeClass('active-order-button');
    }
    $(this).addClass('active-order-button');
});

$('#payment-button .order-button').click(function (e) {
    var buttonArray = $('#payment-button .order-button');
    for (var i = 0 ; i <buttonArray.length;i++){
        $(buttonArray[i]).removeClass('active-order-button');
    }
    $(this).addClass('active-order-button');
});




$('.account-order-button').click(function (e) {
    var buttonArray = $('.account-order-button');
    for (var i = 0 ; i <buttonArray.length;i++){
        $(buttonArray[i]).removeClass('active-account-order-button');
    }
    $(this).addClass('active-account-order-button');
});

$('#email-repeat').on('change', function(e){
            var email_repeat = $(this).val();
            var email = $(this).parent().parent().find('#email').val();
            var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]');
            if (email_repeat == email){
                $.ajax({
                    url: '/user-profile/',
                    type: 'post',
                    data: {
                        email: email_repeat,
                        'csrfmiddlewaretoken': csrfmiddlewaretoken.val()
                    },
                    success: function (response) {
                        if (response.data) {
                            $('body').find('.email_submit').after(response.data)
                        } else {
                            $('.dictionary-content').html('');
                        }
                    }
                })
            }else{
                alert('Введенные данные не совподают')
            }
});
$('.order-button').on('click', function (e) {
    console.log('tut');
    var buttonArray = $('.order-button');
    for (var i = 0 ; i <buttonArray.length;i++){
        $(buttonArray[i]).removeClass('active-order-button');
    }
    $(this).addClass('active-order-button');
});