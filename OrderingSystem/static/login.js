$(document).ready(function(){
    
    $("#loginModal").on('click', '#login-but', function () {
        var username = $('#id_username').val();
        var password = $('#id_password').val();
        var crf = $('#loginModal input[type="hidden"]').val();

        
        $.ajax({
            method: "POST",
            data: {username: username, password:password,csrfmiddlewaretoken:crf},
            url: "/accounts/modal-login/",
            success: function (data) {
                
                if (data=='You have successful logged in.') {
                    location.reload();
                }else{
                    $("#loginModal").html(data);
                };
                
            },
            error:function(xhr,status,error){
               
                alert(xhr.responseText);
            }
        })
    })
})
	