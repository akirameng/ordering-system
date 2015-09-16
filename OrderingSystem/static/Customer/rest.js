$(document).ready(function () {
    var href = location.href; // get the url
    var split = href.split("#"); // split the string; usually there'll be only one # in an url so there'll be only two parts after the splitting
    if (split[1] != null) {
        scrolltocomment();
    }
    $('#close-but').click(function () {
        closeimage();
    })
    $('body').click(function(event){ 
        if (($(event.target).attr('id')=='image-tag'||$(event.target).attr('id')=='black-screen')&&$('#black-screen').css('display')=='block') {
           closeimage();
        };
    })
    $('#comment_cont').click(function(){
        scrolltocomment();
    })
    $('.rest-pic').click(function () {
        $('#image-tag img').attr('src', $('.rest-pic img').attr('src'));
        $('#image-tag').css('display', 'block').animate({
                opacity: "1",
            }, {
                duration: 500,
                queue: false,
                complete: function () {
                    $('#close-but').css('display', 'block');
                }
            }
        );
        $('#black-screen').css('display', 'block').animate({
                opacity: "0.5",
            },
            {duration: 500, queue: false},
            function () {

            }
        );
    })
    $('.dish-pic').click(function () {
        $('#image-tag img').attr('src', $(this).children().attr('src'));
        $('#image-tag').css('display', 'block').animate({
                opacity: "1",
            }, {
                duration: 500,
                queue: false,
                complete: function () {
                    $('#close-but').css('display', 'block');
                }
            }
        );
        $('#black-screen').css('display', 'block').animate({
                opacity: "0.5",
            },
            {duration: 500, queue: false},
            function () {

            }
        );
    })
    $('#load-more-but').click(function(){
        $('html, body').animate({
            scrollTop: $("#comment_form").offset().top
        }, 1000);
        
    })
    $('#id_rating').change(function(){
        var value = $('#id_rating').val();
        if ($.isNumeric(value)) {
            value = parseInt($('#id_rating').val());
            if (value<1||value>5) {
                alert("rating can only be 0 - 5");
                $('#id_rating').val('1'); 
            };
        }else{
            alert("rating has to be an integer");
           $('#id_rating').val('1'); 
        }
        
        
    })
})
function closeimage(){
    $('#black-screen').animate({
                opacity: "0",
            },
            {
                duration: 500,
                queue: false,
                complete: function () {
                    $('#close-but').css('display', 'none');
                    $('#black-screen').css('display', 'none');
                    $('#image-tag').css('display', 'none');
                }
            });
        $('#image-tag').animate({
                opacity: "0",
            },
            {duration: 500, queue: false},
            function () {

            }
        );
}
function scrolltocomment(){
    $('html, body').animate({
            scrollTop: $("#comment-sec").offset().top
        }, 1000);
}
	