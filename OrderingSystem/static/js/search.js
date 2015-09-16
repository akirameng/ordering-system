/**
 * Created by JC on 15-08-08.
 */
$(document).ready(function () {

    $('#id_query').attr('autocomplete', "off");
    $('#id_query').keyup(function () {
        var text = $('#id_query').val();
        if (text != "") {
            var csrf = $("#search_form input[type='hidden']").val();
            $.ajax({
                method: "GET",
                url: "/searchresult/",
                data: {
                    search_text: text,
                    csrfmiddlewaretoken: csrf
                },
                success: function (data) {
                    $('#search-results').html(data);
                },
                error: function (xhr, status, error) {
                    $('#search-results').html(xhr.responseText);
                }
            });
        }
        else {
            $('#search-results').html("");
        }
    });
});