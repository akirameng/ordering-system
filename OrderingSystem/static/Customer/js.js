$(document).ready(function () {
    var href = location.href; // get the url
    var split = href.split("#"); // split the string; usually there'll be only one # in an url so there'll be only two parts after the splitting
    if (split[1] != null) {
        $('#black-screen').css('display', 'block');
        $('#dish-info').attr('dish-id', split[1]).animate({
            left: "0",
        }, {
            duration: 500,
            complete: function () {
                ajax_info(split[1]);
            }
        });

    }
    $('body').click(function(event){
        if ($(event.target).attr('id')=='black-screen'&&$('#black-screen').css('display')=='block') {
            close_sidebar();
        };
    })
    $('#close-but').click(function () {
        close_sidebar();
    })

    $('.one-dish-a').click(function () {
        id = $(this).attr('dish-id');
        $('#black-screen').css('display', 'block');
        $('#dish-info').animate({
                left: "0",
            }, {
                duration: 500,
                complete: function () {
                    ajax_info(id);
                    $('#dish-info').attr('dish-id',id);
                }
            }
        );
    })
    $('.dish-like').click(function () {
        var url = "/dishlist/"+$('#dish-info').attr('dish-id')+"/like";
        $(this).css('font-size', '20px').css('font-weight','bold');
        $.ajax({
            dataType:"json",
            url: url,
            success: function (data) {
                
                $('.dish-like').html(data['liked']);
                dishlikepercentage($('#dish-info').attr('dish-id'),data['liked'],data['unliked'])
            },
            error:function(xhr,status,error){
               
                alert(xhr.responseText);
            }
        })
    })
    $('.dish-unlike').click(function () {
        var url = "/dishlist/"+$('#dish-info').attr('dish-id')+"/unliked";
        $(this).css('font-size', '20px').css('font-weight','bold');
        $.ajax({
            dataType:"json",
            url: url,
            success: function (data) {
                
                $('.dish-unlike').html(data['unliked']);
                dishlikepercentage($('#dish-info').attr('dish-id'),data['liked'],data['unliked'])
            },
            error:function(xhr,status,error){
               
                alert(xhr.responseText);
            }
        })
    })
    $('.add-to-cart').click(function(){
        var vid = String($(this).attr('dish-id'));
        
        var count =$(this).parent().prev().children().val();
        $.ajax({
            method:"POST",
            data:{id:vid,count:count},
            url:"/cookie/",
            success:function(data){
                if (data=='yes') {
                    alert('Sucessfully add to cart')
                };
            },
            error:function(xhr,status,error){
                alert("Fail to add to cart");
            }
        })
    })
    $("#enttag").click(function (){
        //$(this).animate(function(){
        $('html, body').animate({
            scrollTop: $("#Entries").offset().top
        }, 1000);
                //});
    });
    $("#maintag").click(function (){
        //$(this).animate(function(){
        $('html, body').animate({
            scrollTop: $("#Main").offset().top
        }, 1000);
                //});
    });
    $("#destag").click(function (){
        //$(this).animate(function(){
        $('html, body').animate({
            scrollTop: $("#Dessert").offset().top
        }, 1000);
                //});
    });
    $("#drktag").click(function (){
        //$(this).animate(function(){
        $('html, body').animate({
            scrollTop: $("#Drink").offset().top
        }, 1000);
                //});
    });
})
function close_sidebar(){
    $('#black-screen').css('display', 'none');
        $('#dish-info').animate({
            left: "-350px",
        }, 500, function () {
            $('#dish-content').css('display', 'none');
            $('#error').css('display','none');
            $('#loading-pic').css('display', 'block');
            $('.dish-like').css('font-size', '15px');
            $('.dish-unlike').css('font-size', '15px');
        });
}
function ajax_info(id) {
    var url = "/dishlist/" + id + "/?format=json";
    $.ajax({
        dataType: "json",
        data: {id: id},
        url: url,
        success: function (data) {
            //alert(data[0]['price']);
            $('.dish-price').html("&#36;" + data[0]['price']);
            $('.dish-name').html(data[0]['name']);
            $('.dish-like').html(data[0]['liked']);
            $('.dish-unlike').html(data[0]['unliked']);
            $('.dish-descp').html(data[0]['description']);
            $('.dish-img').attr('src', data[0]['image']);
            $('#dish-content').css('display', 'block');
            $('#loading-pic').css('display', 'none');
            var comment="";
            for (var i = 0; i < data[1].length; i++) {
                comment+="<div class='column small-12 one-comment'>";
                comment+= data[1][i]['comment'];
                comment+= "</div><hr>"; 
            };
            $('#dish-comment').html(comment);
        },
        error:function(xhr,status,error){
            if (xhr.responseText!='') {
                $('#loading-pic').css('display', 'none');
                $('#error').css('display','block');
            };
        }
    })
}
function dishlikepercentage(dish_id,like,unlike){
    var percentage = Math.round(parseInt(like)/(parseInt(like)+parseInt(unlike))*100);
    $('.one-dish-a').each(function(){
        if ($(this).attr('dish-id')==dish_id) {
            $($(this).parent().next().children().children()[1]).children().html(percentage+"%<br>Like")
        };
    })
}	