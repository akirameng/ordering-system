$(document).ready(function () {
 $('.rest_pic').click(function(){
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
 $('body').click(function(event){ 
        if (($(event.target).attr('id')=='image-tag'||$(event.target).attr('id')=='black-screen')&&$('#black-screen').css('display')=='block') {
           closeimage();
        };
    }) 
    $('.cuisine_item').click(function(){
        $('#cuisine-btn').html($(this).html());
        $('#cuisine-btn').attr('abb',$(this).attr('abb'))
        filter();
    })
    $('input[type="checkbox"]').click(function(){
        //$('#cuisine-btn').html($(this).html());
        //$('#cuisine-btn').attr('abb',$(this).attr('abb'))
        filter();
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
function filter(){
    url ="/filter"
    $('#loading-pic').css('display','block');
    $('#has_result').css('display','none');
    var name = $('input[type=hidden]').attr('name');
    var value = $('input[type=hidden]').attr('value');
    //alert($('#cuisine-btn').attr('abb'))
    $.ajax({
            dataType:"json",
            method:"POST",
            url: url,
            data:{  
                    category:$('#cuisine-btn').attr('abb'),
                    Provide_Delivery:$('#checkDelivery').is(':checked'),
                    Wifi:$('#checkWifi').is(':checked'),
                    Children_Friendly:$('#checkChildren').is(':checked'),
                    Vegan:$('#checVegan').is(':checked'),
                    GlutenFree:$('#checkGluten').is(':checked'),
                    csrfmiddlewaretoken:value
                },
            success: function (data) {
                
                //alert('result '+data)
                var result ="";
                for (var i = 0; i < data.length; i++) {
                    
                    result +='<div class="restaurant_item row">';
                        result +=' <div class="columns small-10 large-8">';
                            result +=' <a href="'+data[i]['id']+'" class="rest_name">'+data[i]['name']+'</a>';
                            result +='<div style="color: #757575">Cuisine: '+data[i]['category']+'</div>';
                            result +='<div class="rest_address">'+data[i]['city']+':'+data[i]['address']+'</div>';
                            result += '<div class="rest_tags">'
                                result += '<span class="round secondary label" ><a href="'+data[i]['id']+'/dishlist">Menu</a></span>';
                                    result += '<span class="round secondary label" ><a href="'+data[i]['id']+'/#photos">Pictures</a></span>';
                                    result += '<span class="round secondary label" ><a href="'+data[i]['id']+'/#comment">Comment</a></span>';
                                result+='</div>';
                            result+='</div>'
                            result+='<div class="columns small-2 large-4 right rating" >';
                                result+='<div class="row">';
                                    result+='<div class="small-12 columns rating_section">';
                                        result+='<div class="row rating_section">';
                                            result+='<div class="info round label small-centered rate_label" >'+data[i]['rating']+'</div>';
                                            result+='<div class="vote">'+data[i]['vote']+' votes</div> ';
                                        result+='</div>';
                                    result+='</div>';
                                    result+='<div class="column small-12">';
                                    if (data[i]['image']) {
                                        result+='<span class="rest_pic" ><img src="'+data[i]['image']+'"height="60" width="60"></span>';
                                    }
                                    result+='</div>';
                                result+='</div>';
                            result+='</div>';
                        result+='</div>';
                        result+='<hr>';
                };
                if (!data||data.length==0||data[0]==undefined) {
                    result='<p>has no result</p>'
                };
                setTimeout(function(){
                    $('#loading-pic').css('display','none');
                    $('#has_result').css('display','block');
                    $('#has_result .columns').html(result);},500)
                
            },
            error:function(xhr,status,error){
                alert('123')
                //$("#search-results").html(xhr.responseText);
                //alert("Fail to retrieve data, please try again later");
                $('#loading-pic').css('display','none');
                $('#has_result').css('display','block');
            }
        })
}
