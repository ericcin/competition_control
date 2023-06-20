$('.ui.dropdown').dropdown();

$('.message .close').on('click', function() {
    $('.message').hide();
});

$('#new_transaction').click(function () {

        $.ajax({
            method: 'POST',
            url: '/new_transaction/',
//            data: { 'transaction': transaction, 'action': action, 'item': item, 'value1': value1, 'operator': operator, 'value2': value2},
            success: function (resposta) {
                let resultado = JSON.parse(resposta)
                console.log(resultado['result'])
                $('#menu_transaction').append('<div class="item" data-value="' + resultado['result'] + '">' + resultado['result'].toUpperCase() + '</div>')
            },
        });



});

function validate_fields(){
    let action = $('#action').val()
    if($('#transaction').val() == '')
        return false;
    else if(action == '')
        return false;
    else if($('#item').val() == '')
        return false;
    else if(action == "write_item"){
        if($('#value1').val().trim() == '')
            return false;
        else if($('#operator').val() == '')
            return false;
        else if($('#value2').val().trim() == '')
            return false;
    }
    return true;
}

$('#btnRealizarAcao').click(function () {
    let action = $('#action').val()
    if(action == "write_item"){
        $('#selected_item').val($('#item').val());
        $('#value1').val('');
        $('#operator').val('');
        $('#value2').val('');
//        $('#header').text(action.toUpperCase());
        $('#value_item').modal('show');
    }
    else
        active_action();
});

$('#btnCheck').click(function () {
    active_action();
});

function active_action () {

    if(validate_fields()){
        $('#erro').hide();
        let transaction = $('#transaction').val();
        let action = $('#action').val();
        let item = $('#item').val();
        let value1 = 0;
        let operator = 0;
        let value2 = 0;

        if(action == "write_item"){
            value1 = $('#value1').val();
            operator = $('#operator').val();
            value2 = $('#value2').val();
        }

        $.ajax({
            method: 'POST',
            url: '/action/',
            data: { 'transaction': transaction, 'action': action, 'item': item, 'value1': value1, 'operator': operator, 'value2': value2},
            success: function (resposta) {
                let resultado = JSON.parse(resposta)
                console.log(resultado['result'])
                $("#log").val($("#log").val() + "\n" + resultado['result'])
            },
        });
    } else
        $('#erro').show();

};