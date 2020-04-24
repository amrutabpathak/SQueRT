var data = []
var token = ""

jQuery(document).ready(function () {
    $('#input_question').keyup(function (e) {
        if (e.which === 13) {
            $('#btn-process').click()
        }
    });

    $('#btn-process').on('click', function () {
        input_question = $('#input_question').val()
        input_keyword = $('#input_keyword').val()

        $.ajax({
            url: '/predict',
            type: "post",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                "input_question": input_question,
                "input_keyword": input_keyword,
            }),
            beforeSend: function () {
                $('.overlay').show()
                $('#pdf_link').val('')
                $('#snippet').val('')
                $('#predictions').val('')
            },
            complete: function () {
                $('.overlay').hide()
            }
        }).done(function (jsondata, textStatus, jqXHR) {
            console.log(jsondata)
            $('#pdf_link').val(jsondata['pdf_link'])
            $('#snippet').val(jsondata['snippet'])
            $('#predictions').val(jsondata['predictions'])
        }).fail(function (jsondata, textStatus, jqXHR) {
            console.log(jsondata)
            alert(jsondata['responseText'])
        });
        $('#dropdownMenuButton').show();    
    })


})